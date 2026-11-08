import numpy as np, pandas as pd
rng=np.random.default_rng(7)
# name, role, hand, bowl, bat_kph, release_kph, action, conf, era codes (26=2026 squad, 25=2025 title squad, H=2011-17 core), balls bowled/season, balls faced/season, throws/season, keeper_factor
A="Tall, high arm, hit-the-deck"
P=[
["Virat Kohli","BAT","R","",105,0,"","M","26,25,H",0,500,210],
["Rajat Patidar","BAT","R","",110,0,"","M","26,25",0,450,210],
["Devdutt Padikkal","BAT","L","",104,0,"","M","26,25",0,380,210],
["Swastik Chikara","BAT","?","",100,0,"","L","26",0,80,210],
["Phil Salt","WK","R","",115,0,"","M","26,25",0,450,420],
["Jitesh Sharma","WK","R","",108,0,"","M","26,25",0,200,420],
["Jordan Cox","WK","R","",108,0,"","L","26",0,120,420],
["Tim David","BAT","R","",118,0,"","M","26,25",0,160,210],
["Venkatesh Iyer","AR","L","RM",106,118,"Side-on, short run-up","L","26",60,250,210],
["Krunal Pandya","AR","L","SLA",100,88,"Round, flat trajectory","M","26,25",280,100,210],
["Romario Shepherd","AR","R","RFM",115,138,"Open chest, hit-the-deck","M","26,25",130,70,210],
["Jacob Bethell","AR","L","SLA",106,84,"Classical high arm","L","26,25",90,150,210],
["Swapnil Singh","AR","L","SLA",98,82,"Loopy, high arm","L","26,25",120,20,210],
["Mangesh Yadav","AR","?","?",100,128,"Unverified","L","26",100,40,210],
["Satvik Deswal","AR","?","?",98,0,"Unverified","L","26",0,30,210],
["Kanishk Chouhan","AR","?","?",96,0,"Unverified","L","26",0,30,210],
["Vihaan Malhotra","AR","?","?",98,0,"Unverified","L","26",0,30,210],
["Vicky Ostwal","AR","L","SLA",92,80,"High arm, drift","L","26",60,10,210],
["Josh Hazlewood","BOWL","R","RFM",80,138,A,"H","26,25",300,8,210],
["Bhuvneshwar Kumar","BOWL","R","RFM",85,132,"Upright, wrist behind ball (swing)","H","26,25",300,8,210],
["Yash Dayal","BOWL","L","LFM",88,136,"Left-arm, angle across RHB","M","26,25",270,8,210],
["Nuwan Thushara","BOWL","R","RF",78,143,"Low slinging round-arm","H","26,25",180,8,210],
["Jacob Duffy","BOWL","R","RFM",80,137,"Tall, high arm, seam","M","26",150,8,210],
["Rasikh Salam","BOWL","R","RFM",82,136,"Skiddy, round-ish","M","26,25",150,8,210],
["Suyash Sharma","BOWL","R","LB",80,85,"Wrist spin, quick through air","M","26,25",270,8,210],
["Liam Livingstone","AR","R","LB/OB",120,88,"Part-time spin, high arm","L","25",60,220,210],
["Mayank Agarwal","BAT","R","",100,0,"","L","25",0,200,210],
["Lungi Ngidi","BOWL","R","RFM",70,138,"High arm, slower-ball variations","L","25",150,5,210],
["Chris Gayle","BAT","L","",112,0,"","M","H",0,400,210],
["AB de Villiers","WK","R","",115,0,"Part-time keeper","M","H",0,400,300],
["KL Rahul","BAT","R","",104,0,"","L","H",0,300,210],
["Shane Watson","AR","R","RFM",108,135,"Side-on, high arm","M","H",150,250,210],
["Mitchell Starc","BOWL","L","LFM",82,148,"Left-arm, high arm, full-length swing","M","H",150,8,210],
["Yuzvendra Chahal","BOWL","R","LB",60,85,"Wrist spin, flight and loop","M","H",280,8,210],
["Vinay Kumar","BOWL","R","RFM",78,128,"Round-arm, skiddy","L","H",250,8,210],
["Stuart Binny","AR","R","RM",95,128,"Side-on, medium pace","L","H",60,120,210],
["Parthiv Patel","WK","L","",98,0,"","L","H",0,250,420],
["Mandeep Singh","BAT","R","",100,0,"","L","H",0,150,210],
["Sarfaraz Khan","BAT","R","",102,0,"","L","H",0,120,210],
["Travis Head","BAT","L","",108,0,"","L","H",0,120,210],
["Washington Sundar","AR","L","OB",92,85,"Flat off-spin","L","H",240,150,210]]
d=pd.DataFrame(P,columns="player role bat_hand bowl_type est_bat_speed_kph est_release_kph action_class est_confidence era_codes est_balls_bowled_season est_balls_faced_season est_throws_season".split())
def af(a):
    a=a.lower();return 1.10 if "sling" in a else 1.05 if ("open" in a or "round" in a) else 1.0
d["action_factor"]=d.action_class.map(af)
d["keeper_factor"]=np.where(d.role=="WK",1.5,1.0);d["per_throw_weight"]=np.where(d.role=="WK",.25,.5)
EN={"26":"2026 squad","25":"2025 title squad","H":"2011-17 core"}
d["era"]=d.era_codes.map(lambda s:"; ".join(EN[x] for x in s.split(",")))
def comp(r,s=1.0,w=1.0):
    bl=(r.est_release_kph*s/143)**2*r.action_factor*r.est_balls_bowled_season*w/100 if r.est_release_kph>0 else 0
    bt=.35*(r.est_bat_speed_kph*s/118)**2*r.est_balls_faced_season*w/100
    fl=r.per_throw_weight*r.keeper_factor*r.est_throws_season/100
    return bl,bt,fl
c=d.apply(lambda r:comp(r),axis=1,result_type="expand");d["raw"]=c.sum(axis=1);k=100/d.raw.max()
d[["bowling_load","batting_load","fielding_load"]]=(c*k).round(1);d["shoulder_load_index"]=(d.raw*k).round(1)
d["peak_delivery_load_idx"]=np.where(d.est_release_kph>0,((d.est_release_kph/143)**2*d.action_factor*100).round(1),0)
tau,dt=3.0,4.5
def peak(t,n=14):
    L=t/14;F=0;h=[]
    for _ in range(n):F=F*np.exp(-dt/tau)+L;h.append(F)
    return max(h)
d["peak_fatigue_idx"]=[round(peak(t),1) for t in d.shoulder_load_index]
lo,hi=[],[]
for _,r in d.iterrows():
    v=[sum(comp(r,rng.normal(1,.03),rng.lognormal(0,.2)))*k for _ in range(2000)];lo.append(np.percentile(v,5));hi.append(np.percentile(v,95))
d["sli_p05"]=np.round(lo,1);d["sli_p95"]=np.round(hi,1)
q1,q2=d.shoulder_load_index.quantile([.5,.8])
d["relative_risk_band"]=np.where(d.shoulder_load_index>=q2,"High",np.where(d.shoulder_load_index>=q1,"Moderate","Low"))
d["modeled_carry_m_vs135"]=[round(.72*((.95*b+.25*135)/3.6)**2*np.sin(np.radians(60))/9.81,1) for b in d.est_bat_speed_kph]
d["workload_basis"]="assumed typical RCB season for this player, not verified career data"
out=d.drop(columns=["raw","era_codes"]);out.to_csv("/mnt/user-data/outputs/rcb_biomechanics_dataset.csv",index=False);d.to_pickle("d.pkl")
print(len(d));print(d.sort_values("shoulder_load_index",ascending=False)[["player","era","shoulder_load_index","relative_risk_band","sli_p05","sli_p95"]].head(14).to_string())
print(d.groupby("role").shoulder_load_index.agg(["count","mean","max"]).round(1))
for e in ["26","25","H"]:
    s=d[d.era_codes.str.contains(e)];print(e,len(s),round(s.shoulder_load_index.mean(),1),round(s.est_bat_speed_kph.mean(),1),round(s[s.est_release_kph>0].est_release_kph.mean(),1))
print("q",q1,q2)
