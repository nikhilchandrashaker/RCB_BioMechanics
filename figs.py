import pandas as pd,numpy as np,matplotlib;matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
R,K,G="#C8102E","#111111","#D4AF37"
plt.rcParams.update({"font.size":9,"axes.spines.top":False,"axes.spines.right":False})
d=pd.read_pickle("d.pkl")
# F1 scatter
f,a=plt.subplots(figsize=(6.2,3.8))
cm={"BAT":R,"WK":"#2da44e","AR":G,"BOWL":K}
for r in d.itertuples():
    a.scatter(r.est_bat_speed_kph,r.est_release_kph if r.est_release_kph>0 else np.nan,c=cm[r.role],s=50)
    if r.est_release_kph>0:a.annotate(r.player.split()[-1],(r.est_bat_speed_kph,r.est_release_kph),fontsize=7,xytext=(3,3),textcoords="offset points")
a.set_xlabel("Est. bat speed at impact (kph)");a.set_ylabel("Est. release speed (kph)");a.set_title("Bowling output vs batting output (bowlers and all-rounders)")
for k,v in cm.items():a.scatter([],[],c=v,label=k)
a.legend(frameon=False,fontsize=7);f.tight_layout();f.savefig("fig1.png",dpi=200)
# F2 stacked
s=d.sort_values("shoulder_load_index");f,a=plt.subplots(figsize=(6.2,8.8))
a.tick_params(axis="y",labelsize=7);a.barh(s.player,s.bowling_load,color=R,label="Bowling");a.barh(s.player,s.batting_load,left=s.bowling_load,color=K,label="Batting")
a.barh(s.player,s.fielding_load,left=s.bowling_load+s.batting_load,color=G,label="Fielding / keeping")
a.set_xlabel("Shoulder Load Index (squad max = 100)");a.set_title("Season shoulder load by source");a.legend(frameon=False,fontsize=7,loc="lower right");f.tight_layout();f.savefig("fig2.png",dpi=200)
# F3 fatigue
tau,dt=3.0,4.5;f,a=plt.subplots(figsize=(6.2,3.6))
for n,c in [("Josh Hazlewood",R),("Bhuvneshwar Kumar",K),("Nuwan Thushara",G),("Phil Salt","#2da44e"),("Virat Kohli","#888")]:
    t=d[d.player==n].shoulder_load_index.iloc[0]/14;F=0;h=[]
    for _ in range(14):F=F*np.exp(-dt/tau)+t;h.append(F)
    a.plot(range(1,15),h,color=c,marker="o",ms=3,label=n)
a.set_xlabel("Match number");a.set_ylabel("Fatigue index");a.set_title("Modeled shoulder fatigue accumulation (14 matches, 4.5-day spacing)");a.legend(frameon=False,fontsize=7);f.tight_layout();f.savefig("fig3.png",dpi=200)
# F4 carry
f,a=plt.subplots(figsize=(6.2,3.6));b=np.linspace(80,125,50)
for vin,c in [(80,"#888"),(110,G),(140,R)]:
    a.plot(b,0.72*((0.95*b+0.25*vin)/3.6)**2*np.sin(np.radians(60))/9.81,color=c,label=f"incoming {vin} kph")
a.axhspan(100,110,color=G,alpha=.15);a.set_xlabel("Bat speed at impact (kph)");a.set_ylabel("Modeled carry (m)");a.set_title("Impact model: carry vs bat speed (30 deg launch)");a.legend(frameon=False,fontsize=7);f.tight_layout();f.savefig("fig4.png",dpi=200)
# F5 diagram
f,a=plt.subplots(figsize=(6.4,3.3));a.axis("off");a.set_xlim(0,10);a.set_ylim(0,5)
bx=[("Legs & trunk\n(ground force,\nrotation)",0.2,3.3,R),("Scapula\n(stabilizers)",2.6,3.3,K),("Glenohumeral joint\n(internal rotation,\nhorizontal adduction)",5.0,3.3,R),("Release / bat\nimpact",7.6,3.3,K)]
for t,x,y,c in bx:
    a.add_patch(FancyBboxPatch((x,y),2.1,1.3,boxstyle="round,pad=0.05",fc=c,ec=G,lw=1.5));a.text(x+1.05,y+.65,t,ha="center",va="center",color="w",fontsize=7)
for x in [2.35,4.75,7.15]:a.annotate("",(x+.25,3.95),(x,3.95),arrowprops=dict(arrowstyle="->",color=G,lw=2))
mods=[("Speed term\n(v/143)^2",1.2),("Action factor a\n(sling 1.10, open/round 1.05)",4.0),("Workload\n(balls, swings, throws)",7.0)]
for t,x in mods:
    a.add_patch(FancyBboxPatch((x-.9,1.0),2.2,1.1,boxstyle="round,pad=0.05",fc="white",ec=R,lw=1.5));a.text(x+.2,1.55,t,ha="center",va="center",fontsize=7)
    a.annotate("",(5.5 if x>3 else 5.0,3.25),(x+.2,2.2),arrowprops=dict(arrowstyle="->",color=R))
a.text(5,.35,"SLI = bowling + 0.35 x batting + fielding   ->   fatigue F(t+1) = F(t) exp(-4.5/3) + L",ha="center",fontsize=7.5,color=K)
a.set_title("Shoulder load model: kinetic chain and load terms");f.tight_layout();f.savefig("fig5.png",dpi=200)
# F6 intervals
s=d.sort_values("shoulder_load_index",ascending=False).head(12).iloc[::-1];f,a=plt.subplots(figsize=(6.2,3.8))
a.hlines(s.player,s.sli_p05,s.sli_p95,color=R,lw=3);a.scatter(s.shoulder_load_index,s.player,color=K,zorder=3)
a.set_xlabel("Shoulder Load Index (point = base, bar = 5th-95th pct)");a.set_title("Monte Carlo uncertainty, top 12 (speed 3% sd, workload lognormal 0.2)");f.tight_layout();f.savefig("fig6.png",dpi=200)
# F7 role boxplot + era means
f,(a,b)=plt.subplots(1,2,figsize=(6.4,3.4),gridspec_kw={"width_ratios":[1.3,1]})
roles=["BAT","WK","AR","BOWL"];data=[d[d.role==r].shoulder_load_index for r in roles]
bp=a.boxplot(data,tick_labels=["Batter","Keeper","All-rounder","Bowler"],patch_artist=True,medianprops=dict(color=G,lw=2))
for p in bp["boxes"]:p.set(facecolor=R,alpha=.8)
a.set_ylabel("Shoulder Load Index");a.set_title("SLI by role",fontsize=9)
ev=[("2026","26"),("2025 title","25"),("2011-17","H")]
b.bar([e[0] for e in ev],[d[d.era_codes.str.contains(e[1])].shoulder_load_index.mean() for e in ev],color=[R,K,G]);b.set_title("Mean SLI by era group",fontsize=9);b.tick_params(axis="x",labelsize=7)
f.tight_layout();f.savefig("fig7.png",dpi=200)
