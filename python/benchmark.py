import sys
import time

def bubble(a):
    for i in range(len(a)-1):
        cambio=False
        for j in range(len(a)-i-1):
            if a[j]>a[j+1]:
                a[j],a[j+1]=a[j+1],a[j]
                cambio=True
        if not cambio:
            break

def merge(a):
    b=[0.0]*len(a)
    w=1
    while w<len(a):
        for s in range(0,len(a),2*w):
            m=min(s+w,len(a))
            e=min(s+2*w,len(a))
            i,j,k=s,m,s
            while i<m and j<e:
                if a[i]<=a[j]:
                    b[k]=a[i]
                    i+=1
                else:
                    b[k]=a[j]
                    j+=1
                k+=1
            while i<m:
                b[k]=a[i]
                i+=1
                k+=1
            while j<e:
                b[k]=a[j]
                j+=1
                k+=1
        a,b=b,a
        w*=2
    return a

class Nodo:
    __slots__=("v","izq","der","cuenta")
    def __init__(self,v):
        self.v=v
        self.izq=None
        self.der=None
        self.cuenta=1

def tree(a):
    if not a:
        return
    raiz=Nodo(a[0])
    for v in a[1:]:
        p=raiz
        while True:
            if v==p.v:
                p.cuenta+=1
                break
            if v<p.v:
                if p.izq is None:
                    p.izq=Nodo(v)
                    break
                p=p.izq
            else:
                if p.der is None:
                    p.der=Nodo(v)
                    break
                p=p.der
    pila=[]
    p=raiz
    k=0
    while p is not None or pila:
        while p is not None:
            pila.append(p)
            p=p.izq
        p=pila.pop()
        for _ in range(p.cuenta):
            a[k]=p.v
            k+=1
        p=p.der

def hundir(a,r,n):
    while 2*r+1<n:
        h=2*r+1
        if h+1<n and a[h]<a[h+1]:
            h+=1
        if a[r]>=a[h]:
            return
        a[r],a[h]=a[h],a[r]
        r=h

def heap(a):
    for i in range(len(a)//2-1,-1,-1):
        hundir(a,i,len(a))
    for n in range(len(a)-1,0,-1):
        a[0],a[n]=a[n],a[0]
        hundir(a,0,n)

def counting(a):
    c=[0]*100001
    for v in a:
        x=round(v*100)
        if x< -50000 or x>50000:
            raise ValueError("Fuera de rango")
        c[x+50000]+=1
    k=0
    for i,n in enumerate(c):
        if n:
            a[k:k+n]=[(i-50000)/100.0]*n
            k+=n

def datos(n,seed):
    a=[]
    for _ in range(n):
        seed=(seed*1664525+1013904223)&0xffffffff
        a.append(((seed%100001)-50000)/100.0)
    return a

def memoria():
    if sys.platform=="win32":
        import ctypes
        from ctypes import wintypes
        class C(ctypes.Structure):
            _fields_=[("cb",wintypes.DWORD),("PageFaultCount",wintypes.DWORD),("PeakWorkingSetSize",ctypes.c_size_t),("WorkingSetSize",ctypes.c_size_t),("QuotaPeakPagedPoolUsage",ctypes.c_size_t),("QuotaPagedPoolUsage",ctypes.c_size_t),("QuotaPeakNonPagedPoolUsage",ctypes.c_size_t),("QuotaNonPagedPoolUsage",ctypes.c_size_t),("PagefileUsage",ctypes.c_size_t),("PeakPagefileUsage",ctypes.c_size_t)]
        c=C()
        c.cb=ctypes.sizeof(c)
        return c.PeakWorkingSetSize/1048576 if ctypes.windll.psapi.GetProcessMemoryInfo(ctypes.windll.kernel32.GetCurrentProcess(),ctypes.byref(c),c.cb) else -1
    import resource
    v=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    return v/1048576 if sys.platform=="darwin" else v/1024

if __name__=="__main__":
    alg=sys.argv[1]
    n=int(sys.argv[2])
    seed=int(sys.argv[3]) if len(sys.argv)>3 else 42
    metodos={"bubble":bubble,"merge":merge,"tree":tree,"heap":heap,"counting":counting}
    if alg=="bubble" and n>5000:
        raise SystemExit("Limite de seguridad: 5000")
    a=datos(n,seed)
    s=time.perf_counter()
    res=metodos[alg](a)
    if res is not None:
        a=res
    t=time.perf_counter()-s
    ok=all(a[i]<=a[i+1] for i in range(len(a)-1))
    print(f"python,{alg},{n},{t:.6f},{memoria():.3f},{'si' if ok else 'no'}")
    if not ok:
        raise SystemExit(4)
