#include <algorithm>
#include <chrono>
#include <cmath>
#include <stdexcept>
#include <cstdint>
#include <cstdlib>
#include <fstream>
#include <iomanip>
#include <iostream>
#include <string>
#include <vector>
#ifdef _WIN32
#include <windows.h>
#include <psapi.h>
#else
#include <sys/resource.h>
#endif
using namespace std;
using V=vector<double>;
void bubble(V& a){for(size_t i=0;i+1<a.size();i++){bool cambio=false;for(size_t j=0;j+i+1<a.size();j++)if(a[j]>a[j+1]){swap(a[j],a[j+1]);cambio=true;}if(!cambio)break;}}
void merge_sort(V& a){V b(a.size());for(size_t w=1;w<a.size();w*=2){for(size_t s=0;s<a.size();s+=2*w){size_t m=min(s+w,a.size()),e=min(s+2*w,a.size()),i=s,j=m,k=s;while(i<m&&j<e)b[k++]=a[i]<=a[j]?a[i++]:a[j++];while(i<m)b[k++]=a[i++];while(j<e)b[k++]=a[j++];}a.swap(b);if(w>a.size()/2)break;}}
struct Nodo{double x;int l=-1,r=-1;uint32_t cuenta=1;};
void tree_sort(V& a){if(a.empty())return;vector<Nodo> t;t.reserve(min(a.size(),size_t(100001)));t.push_back({a[0]});for(size_t i=1;i<a.size();i++){int p=0;while(true){if(a[i]==t[p].x){t[p].cuenta++;break;}int q=a[i]<t[p].x?t[p].l:t[p].r;if(q<0){int z=(int)t.size();if(a[i]<t[p].x)t[p].l=z;else t[p].r=z;t.push_back({a[i]});break;}p=q;}}vector<int> pila;int p=0;size_t k=0;while(p>=0||!pila.empty()){while(p>=0){pila.push_back(p);p=t[p].l;}p=pila.back();pila.pop_back();for(uint32_t i=0;i<t[p].cuenta;i++)a[k++]=t[p].x;p=t[p].r;}}
void hundir(V& a,size_t r,size_t n){while(2*r+1<n){size_t h=2*r+1;if(h+1<n&&a[h]<a[h+1])h++;if(a[r]>=a[h])break;swap(a[r],a[h]);r=h;}}
void heap_sort(V& a){for(size_t i=a.size()/2;i>0;i--)hundir(a,i-1,a.size());for(size_t n=a.size();n>1;n--){swap(a[0],a[n-1]);hundir(a,0,n-1);}}
void counting_sort(V& a){vector<size_t> c(100001);for(double v:a){long x=lround(v*100);if(x< -50000||x>50000)throw runtime_error("Fuera de rango");c[x+50000]++;}size_t p=0;for(int i=0;i<=100000;i++)for(size_t j=0;j<c[i];j++)a[p++]=(i-50000)/100.0;}
V datos(size_t n,uint32_t seed){V a(n);for(double& v:a){seed=seed*1664525u+1013904223u;v=(int(seed%100001u)-50000)/100.0;}return a;}
double memoria(){
#ifdef _WIN32
PROCESS_MEMORY_COUNTERS_INFO c{};return GetProcessMemoryInfo(GetCurrentProcess(),(PROCESS_MEMORY_COUNTERS*)&c,sizeof(c))?double(c.PeakWorkingSetSize)/1048576:-1;
#else
ifstream f("/proc/self/status");string s;while(getline(f,s))if(s.rfind("VmHWM:",0)==0)return stod(s.substr(6))/1024;struct rusage r{};getrusage(RUSAGE_SELF,&r);
#ifdef __APPLE__
return double(r.ru_maxrss)/1048576;
#else
return double(r.ru_maxrss)/1024;
#endif
#endif
}
int main(int argc,char** argv){if(argc<3){cerr<<"Uso: benchmark algoritmo cantidad [semilla]\n";return 2;}try{string alg=argv[1];size_t n=stoull(argv[2]);uint32_t seed=argc>3?stoul(argv[3]):42;V a=datos(n,seed);auto s=chrono::steady_clock::now();if(alg=="bubble")bubble(a);else if(alg=="merge")merge_sort(a);else if(alg=="tree")tree_sort(a);else if(alg=="heap")heap_sort(a);else if(alg=="counting")counting_sort(a);else throw runtime_error("Algoritmo desconocido");double t=chrono::duration<double>(chrono::steady_clock::now()-s).count();bool ok=is_sorted(a.begin(),a.end());cout<<fixed<<setprecision(6)<<"cpp,"<<alg<<","<<n<<","<<t<<","<<memoria()<<","<<(ok?"si":"no")<<"\n";return ok?0:4;}catch(const exception& e){cerr<<e.what()<<"\n";return 1;}}
