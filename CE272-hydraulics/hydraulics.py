"""수리학 계산 도구. SI 단위, 식·가정·잔차를 드러내는 교육용 계산.

관 마찰계수는 Darcy 계수. 관수로 Re<2100은 층류, Re>4000은 난류 모형 사용.
천이영역은 단일 마찰계수로 확정하지 않음. 수로의 x_up은 상류 방향 거리.
"""
import math
import numpy as np
import pandas as pd
from scipy.optimize import brentq

G = 9.81
API_VERSION = '1'


def positive(**values):
    if any(not np.isfinite(v) or v <= 0 for v in values.values()):
        raise ValueError('유한한 양수 필요: ' + ', '.join(values))


def area_pipe(D):
    positive(D=D)
    return math.pi * D**2 / 4


def reynolds(Q, D, nu):
    positive(D=D, nu=nu)
    if not np.isfinite(Q):
        raise ValueError('유한한 유량 필요')
    return abs(Q) / area_pipe(D) * D / nu


def darcy_factor(Re, relative_roughness=0):
    """층류 64/Re 또는 Colebrook 잔차의 양의 근. 천이영역은 계산 중단."""
    positive(Re=Re)
    if not np.isfinite(relative_roughness) or not 0 <= relative_roughness < 0.1:
        raise ValueError('상대조도 범위 확인: 0 이상 0.1 미만')
    if Re < 2100:
        return 64 / Re
    if Re <= 4000:
        raise ValueError('천이영역: 단일 마찰계수 확정 불가')
    def residual(f):
        return 1/math.sqrt(f) + 2*math.log10(relative_roughness/3.7 + 2.51/(Re*math.sqrt(f)))
    return brentq(residual, 0.002, 0.2, xtol=1e-14)


def pipe_loss(Q, L, D, nu=1.006e-6, epsilon=0, minor_K=0, fixed_f=None):
    """부호 있는 수두손실. 흐름 반전 시 부호 반전, 손실 크기는 비음수."""
    positive(L=L, D=D, nu=nu)
    if not np.isfinite([Q, epsilon, minor_K]).all() or epsilon < 0 or minor_K < 0:
        raise ValueError('유량·조도·국부손실계수 확인')
    if Q == 0:
        return 0.0
    f = darcy_factor(reynolds(Q, D, nu), epsilon/D) if fixed_f is None else fixed_f
    positive(f=f)
    V = Q/area_pipe(D)
    return math.copysign((f*L/D + minor_K)*V**2/(2*G), Q)


def turbulent_flow(head, segments, nu=1.006e-6, exit_coefficient=0.):
    """직렬 관로의 난류 유량. 각 구간 Re>4000인 해만 허용.

    segments: [{L,D,epsilon,minor_K}, ...]. 출구 속도수두 계수는
    exit_coefficient로 별도 명시. 큰 수조 사이의 출구손실 K=1과 중복 산입 금지.
    """
    positive(head=head, nu=nu)
    if not np.isfinite(exit_coefficient) or exit_coefficient<0:
        raise ValueError('출구 속도수두 계수는 유한한 비음수 필요')
    if not segments:
        raise ValueError('한 구간 이상 필요')
    lower = max(4000.001*nu/s['D']*area_pipe(s['D']) for s in segments)
    def residual(Q):
        velocity_head=exit_coefficient*(Q/area_pipe(segments[-1]['D']))**2/(2*G)
        return sum(pipe_loss(Q, nu=nu, **s) for s in segments) + velocity_head - head
    if residual(lower) >= 0:
        raise ValueError('난류 가정 범위 밖: 층류·천이영역 검토 필요')
    upper = max(lower*2, 0.01)
    for _ in range(60):
        if residual(upper) >= 0:
            break
        upper *= 2
    else:
        raise ValueError('유량 탐색 범위 확인 필요')
    return brentq(residual, lower, upper, xtol=1e-13)


def pipe_resistance(L, D, f):
    positive(L=L, D=D, f=f)
    return 8*f*L/(math.pi**2*G*D**5)


def parallel_fixed(head, lengths, diameters, factors):
    positive(head=head)
    if not len(lengths)==len(diameters)==len(factors) or len(lengths)==0:
        raise ValueError('구간별 길이·직경·마찰계수 개수 일치 필요')
    K = np.array([pipe_resistance(L,D,f) for L,D,f in zip(lengths,diameters,factors)])
    return np.sqrt(head/K)


HC_L = np.array([1000.,1000.,100.,1000.,1000.])
HC_D = np.array([.5,.4,.4,.5,.3])
HC_F = np.array([.012,.012,.012,.012,.013])
HC_Q0 = np.array([.5,.5,.4,.9,.1])
# global direction: A→C, A→B, B→C, C→D, B→D
HC_C = np.array([[-1.,1.,1.,0.,0.],[0.,0.,-1.,-1.,1.]])
HC_B = np.array([[-1.,-1.,0.,0.,0.], [0.,1.,-1.,0.,-1.],
                 [1.,0.,1.,-1.,0.], [0.,0.,0.,1.,1.]])


def hardy_cross(Q0=None, factors=None, tolerance=1e-9, maxiter=200):
    """원본 Excel의 두 폐회로·공유관. 고정 f, 동시 보정 방식.

    두 회로에 따로 저장한 공유관의 부호 대신 한 전역 유량과 회로 행렬 사용.
    보정은 절점 연속식을 보존. 폐회로 수두잔차로 수렴 판단.
    """
    Q = HC_Q0.copy() if Q0 is None else np.asarray(Q0,dtype=float).copy()
    f = HC_F if factors is None else np.asarray(factors,dtype=float)
    if Q.shape!=(5,) or f.shape!=(5,) or not np.isfinite(Q).all():
        raise ValueError('관 5개의 유한한 유량·마찰계수 필요')
    positive(tolerance=tolerance)
    K = np.array([pipe_resistance(L,D,v) for L,D,v in zip(HC_L,HC_D,f)])
    demand = HC_B@HC_Q0
    if not np.allclose(HC_B@Q,demand,atol=1e-10,rtol=0):
        raise ValueError('초기 유량의 절점 연속식 확인 필요')
    rows=[]
    for k in range(maxiter+1):
        h = K*Q*abs(Q)
        residual = HC_C@h
        derivative = (HC_C**2)@(2*K*abs(Q))
        if np.any(derivative==0):
            raise ValueError('회로 보정 분모 0: 초기 유량 확인 필요')
        delta = -residual/derivative
        row={'iteration':k, **{'Q%d'%(i+1):v for i,v in enumerate(Q)},
             'loop_I':residual[0], 'loop_II':residual[1],
             'delta_I':delta[0], 'delta_II':delta[1],
             'mass_residual':float(np.max(abs(HC_B@Q-demand)))}
        rows.append(row)
        if max(abs(residual))<tolerance:
            return pd.DataFrame(rows)
        Q += HC_C.T@delta
    raise ValueError('반복 한도: 회로 방향·가정·허용오차 확인 필요')


def section(y, b, z=0):
    """사다리꼴/직사각형: z는 수평/수직 측면경사, 수심은 수직 방향."""
    positive(y=y,b=b)
    if not np.isfinite(z) or z<0:
        raise ValueError('유한한 비음수 측면경사 필요')
    A = y*(b+z*y)
    P = b+2*y*math.sqrt(1+z*z)
    return {'A':A, 'P':P, 'R':A/P, 'T':b+2*z*y}


def manning(y,b,z,n,S0):
    positive(n=n)
    if not np.isfinite(S0) or S0<0:
        raise ValueError('등류 계산의 비음수 경사 필요')
    s=section(y,b,z)
    return s['A']/n*s['R']**(2/3)*math.sqrt(S0)


def normal_depth(Q,b,z,n,S0):
    positive(Q=Q,n=n,S0=S0)
    upper=1.
    while manning(upper,b,z,n,S0)<Q:
        upper*=2
        if upper>1e6:raise ValueError('등류수심 탐색 범위 확인 필요')
    return brentq(lambda y:manning(y,b,z,n,S0)-Q,1e-6,upper,xtol=1e-13)


def froude(Q,y,b,z=0):
    s=section(y,b,z)
    return abs(Q)/s['A']/math.sqrt(G*s['A']/s['T'])


def critical_depth(Q,b,z=0):
    positive(Q=Q)
    upper=1.
    while froude(Q,upper,b,z)>1:upper*=2
    return brentq(lambda y:froude(Q,y,b,z)-1,1e-6,upper,xtol=1e-13)


def specific_energy(Q,y,b=1.,z=0):
    s=section(y,b,z)
    return y+(Q/s['A'])**2/(2*G)


def specific_force(Q,y,b):
    positive(y=y,b=b)
    return b*y*y/2+Q*Q/(G*b*y)


def conjugate_depth(Q,y1,b):
    Fr=froude(Q,y1,b)
    if Fr<=1:raise ValueError('도수 전 사류 수심 필요: Fr>1')
    return y1/2*(math.sqrt(1+8*Fr*Fr)-1)


def circular_ratios(theta):
    """θ는 물에 젖은 중심각(rad). 만관 극한은 θ=2π."""
    theta=np.asarray(theta,dtype=float)
    if not np.isfinite(theta).all() or np.any(theta<=0) or np.any(theta>2*np.pi):
        raise ValueError('0<theta<=2π 필요, 단위 rad 확인')
    V=((theta-np.sin(theta))/theta)**(2/3)
    Q=(theta-np.sin(theta))**(5/3)/(2*np.pi*theta**(2/3))
    return Q,V,(1-np.cos(theta/2))/2


def circular_maxima():
    q=brentq(lambda t:5*t*(1-np.cos(t))-2*(t-np.sin(t)),np.pi,2*np.pi-1e-8)
    v=brentq(lambda t:np.sin(t)-t*np.cos(t),np.pi,2*np.pi-1e-8)
    return pd.DataFrame([{'target':label,'theta_rad':t,'theta_deg':np.degrees(t),
                          'Q_Qfull':float(circular_ratios(t)[0]),
                          'V_Vfull':float(circular_ratios(t)[1]),
                          'y_D':float(circular_ratios(t)[2])} for label,t in [('max Q',q),('max V',v)]])


def friction_slope(Q,y,b,z,n):
    positive(n=n)
    s=section(y,b,z)
    return (n*Q/s['A'])**2/s['R']**(4/3)


def direct_step(depths,Q=30.,b=10.,z=2.,n=.013,S0=.001):
    ys=np.asarray(depths,dtype=float)
    if ys.ndim!=1 or len(ys)<2:raise ValueError('두 수심 이상 필요')
    rows=[];x=0.;previous=None
    for y in ys:
        E=specific_energy(Q,y,b,z);Sf=friction_slope(Q,y,b,z,n);Fr=froude(Q,y,b,z)
        row={'y':y,'E':E,'Sf':Sf,'Fr':Fr,'x_up':x,'dx_up':0.,'residual':0.}
        if previous is not None:
            if (Fr*Fr-1)*(previous['Fr']**2-1)<=0 or (S0-Sf)*(S0-previous['Sf'])<=0:
                raise ValueError('한계수심·등류수심을 가로지르는 구간 분리 필요')
            mean=(Sf+previous['Sf'])/2
            if abs(S0-mean)<1e-12:raise ValueError('등류수심 근처: 직접축차 분모·간격 검토 필요')
            dx=(previous['E']-E)/(S0-mean);x+=dx
            row.update(x_up=x,dx_up=dx,residual=E-previous['E']+(S0-mean)*dx)
        rows.append(row);previous=row
    return pd.DataFrame(rows)


def standard_step(x_up,Q=30.,b=10.,z=2.,n=.013,S0=.001,y_down=5.):
    """원본 M1 예제용 표준축차. 상류 방향, 상류 수심은 yn과 직전 수심 사이.

    다른 수면형에는 경계·계산 방향·근의 가지를 새로 선택해야 함.
    """
    xs=np.asarray(x_up,dtype=float)
    if xs.ndim!=1 or len(xs)<2 or xs[0]!=0 or np.any(np.diff(xs)<=0):
        raise ValueError('0부터 증가하는 상류 방향 거리 필요')
    yn=normal_depth(Q,b,z,n,S0);yc=critical_depth(Q,b,z)
    if not y_down>yn>yc:raise ValueError('이 계산기는 M1 경계조건용: y_down>yn>yc 필요')
    y=y_down;rows=[{'x_up':0.,'y':y,'residual':0.,'Fr':froude(Q,y,b,z)}]
    for i in range(1,len(xs)):
        dx=xs[i]-xs[i-1];oldE=specific_energy(Q,y,b,z);oldSf=friction_slope(Q,y,b,z,n)
        def residual(v):
            return specific_energy(Q,v,b,z)-oldE+(S0-(oldSf+friction_slope(Q,v,b,z,n))/2)*dx
        if residual(yn+1e-10)*residual(y)>=0:
            raise ValueError('M1 근의 구간 확보 실패: 거리 스텝 축소 필요')
        y=brentq(residual,yn+1e-10,y,xtol=1e-12)
        rows.append({'x_up':xs[i],'y':y,'residual':residual(y),'Fr':froude(Q,y,b,z)})
    return pd.DataFrame(rows)


def model_ratios(Lr,Tr,rho_r=1.):
    """모든 비는 원형/모형. 기하학적 상사만으로 시간비 결정 불가."""
    positive(Lr=Lr,Tr=Tr,rho_r=rho_r)
    return {'Lr':Lr,'Tr':Tr,'Vr':Lr/Tr,'Qr':Lr**3/Tr,
            'Fr_force':rho_r*Lr**4/Tr**2,'Pr_power':rho_r*Lr**5/Tr**3}
