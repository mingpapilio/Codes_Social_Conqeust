library(ape)
library(geiger)
library(nlme)
library(phytools)
library(phylolm)
library(MuMIn)
library(AICcmodavg)
library(mcgibbsit)
library(phylopath)
#vif.phyloglm(https://github.com/mrhelmus/phylogeny_manipulation/blob/master/AIC_func.r)

setwd("")
newdata_global<-read.csv("global_avian_6553.csv",row.names=1)
newtree_global<-read.nexus("global_avian_6553.nex")
#############################################
#harsh <0.25
newdata_harsh<- subset(newdata_global, (Clade %in% c("Accipitridae","BC7","Furnaridae","M4","P10","P13P14P16","P17P18","Rallidae",
                                                     "RallidaeHeliornithidae","S13","Alcedinidae","Apodidae","BC6","CC8","S12")))
check<-name.check(newtree_global,newdata_harsh)
tips_pruned<-check$tree_not_data
newtree_harsh<-drop.tip(newtree_global,tips_pruned)
#PGLS
model<-phylolm(scale(range_size)~social_system+scale(pre)+scale(pre_var_among)+scale(pre_var_within)+scale(tmp)+
                 scale(str)+scale(dtr)+scale(body_mass),data=newdata_harsh,phy=newtree_harsh,model="lambda",lower.bound=1e-15)
summary(model)
vif.phyloglm(model)
#AIC model average
dd<-MuMIn::dredge(model)
bb<-MuMIn::model.avg(dd)
summary(bb)
#check climate and ss
model_ss<-phyloglm(social_system~scale(pre)+scale(pre_var_among)+scale(pre_var_within)+scale(tmp)+
                     scale(dtr)+scale(str)+scale(body_mass),phy=newtree_harsh,data=newdata_harsh,
                   method="logistic_MPLE",btol=30)
summary(model_ss)
vif.phyloglm(model_ss)
#social_system
newdata_harsh$pre_std<-scale(newdata_harsh$pre)
newdata_harsh$among_std<-scale(newdata_harsh$pre_var_among)
newdata_harsh$within_std<-scale(newdata_harsh$pre_var_within)
newdata_harsh$tmp_std<-scale(newdata_harsh$tmp)
newdata_harsh$str_std<-scale(newdata_harsh$str)
newdata_harsh$dtr_std<-scale(newdata_harsh$dtr)
newdata_harsh$body_mass_std<-scale(newdata_harsh$body_mass)

var_list<-c("pre_std","among_std","within_std","tmp_std","str_std","dtr_std","body_mass_std")

find_all_cb<-function(var_list){
  xx<-seq(1,length(var_list))
  findcb<-function(x){
    all.comb<-combn(var_list,x)
    xy.list <- split(t(all.comb), seq(ncol(all.comb)))
    names(xy.list)<-paste(x,seq(1,length(xy.list)),sep="-")
    return(xy.list)
  }
  return(do.call(c,lapply(xx,findcb)))
}

nullmodel<-list(1)
names(nullmodel)<-"0-1"
qq<-find_all_cb(var_list)

f_hb<-function(x){
  model_coop_hb<-phyloglm(social_system~.,newdata_harsh[,c("social_system",as.vector(unlist(x)))],newtree_harsh,method="logistic_MPLE",btol=30)
  #return(summary(model_coop_hb))
  mAIC<-AIC(model_coop_hb)
  mAICc<-mAIC+(2*(length(unlist(x))+1)^2+2*(length(unlist(x))+1))/(nrow(newdata_harsh)-(1+length(unlist(x)))-1)
  return(mAICc)
}

model_null<-phyloglm(social_system~1,newdata_harsh,newtree_harsh,method="logistic_MPLE",btol=30)
AICc_null<-AIC(model_null)+(2*1^2+2*1)/(nrow(newdata_harsh)-1-1)
names(AICc_null)<-"Null"
model_name_null<-as.vector("Null")
names(model_name_null)<-"Null"

aiclist_hb<-rapply(qq,f_hb)
aiclist_hb<-c(aiclist_hb,AICc_null)
modellist_hb<-rapply(qq,paste,collapse="+")
modellist_hb<-c(modellist_hb,model_name_null)

hbaic<-data.frame(rank=seq(1,length(aiclist_hb)),
                  model=unlist(lapply(names(sort(aiclist_hb)),function(x){modellist_hb[names(modellist_hb)==x]})),
                  AICc=sort(aiclist_hb))
hbaic$dAICc<-hbaic$AICc-min(hbaic$AICc)
hbaic$Weight<-exp(-0.5*hbaic$dAICc)/sum(exp(-0.5*hbaic$dAICc))
hbaic$Accuw<-NA
for(i in 1:length(hbaic$Weight)){hbaic$Accuw[i]<-sum(hbaic$Weight[1:i])}
hbaic

f_avg<-function(x1,Cand.mods){
  estimate=modavg(cand.set = Cand.mods,parm=x1)$Mod.avg.beta
  se=modavg(cand.set = Cand.mods,parm=x1)$Uncond.SE
  z=estimate/se
  p=2*pnorm(-abs(z))
  out<-data.frame(Predictor=x1,Estimate=estimate,SE=se,Z=z,P=p)
  return(out)
}

#only include the model which dAICc<2
fm1<-phyloglm(social_system~pre_std+among_std+within_std+tmp_std+dtr_std+body_mass_std,newdata_harsh,newtree_harsh,method="logistic_MPLE",btol=30)
fm2<-phyloglm(social_system~pre_std+among_std+within_std+tmp_std+str_std+dtr_std+body_mass_std,newdata_harsh,newtree_harsh,method="logistic_MPLE",btol=30)
fm3<-phyloglm(social_system~pre_std+among_std+tmp_std+str_std+dtr_std+body_mass_std,newdata_harsh,newtree_harsh,method="logistic_MPLE",btol=30)
fm4<-phyloglm(social_system~pre_std+among_std+tmp_std+dtr_std+body_mass_std,newdata_harsh,newtree_harsh,method="logistic_MPLE",btol=30)
fm5<-phyloglm(social_system~pre_std+among_std+within_std+tmp_std+body_mass_std,newdata_harsh,newtree_harsh,method="logistic_MPLE",btol=30)
fm6<-phyloglm(social_system~pre_std+among_std+tmp_std+str_std+dtr_std,newdata_harsh,newtree_harsh,method="logistic_MPLE",btol=30)

Cand.mods <- list("fm1" = fm1, "fm2" = fm2, "fm3" = fm3, "fm4" = fm4, "fm5" = fm5, "fm6" = fm6)

f_avg("(Intercept)",Cand.mods)
f_avg("pre_std",Cand.mods)
f_avg("among_std",Cand.mods)
f_avg("within_std",Cand.mods)
f_avg("tmp_std",Cand.mods)
f_avg("dtr_std",Cand.mods)
f_avg("str_std",Cand.mods)
f_avg("body_mass_std",Cand.mods)

#N=2426, phylopath
newdata_harsh$ss<-as.factor(newdata_harsh$social_system)
#define model set
m <- define_model_set(
  null=c(),
  one=c(range_size~ss),
  .common=c(ss~pre+pre_var_among+tmp+dtr,range_size~pre+pre_var_among+pre_var_within+tmp+str)
)
positions <- data.frame(
  name = c("tmp","pre_var_within","pre","pre_var_among","str","dtr" ,"ss", "range_size"),
  x = c(1:3,5:7, 4, 4),
  y = c(3,3,3,3,3,3, 2, 1)
)
plot_model_set(m, manual_layout = positions, edge_width = 0.5)
p <- phylo_path(m, newdata_harsh, newtree_harsh,model="lambda")
s<-summary(p)
plot(s)

avg <- average(p,cut_off=2 ,avg_method="conditional")
plot(avg, algorithm = 'mds',manual_layout = positions)
coef_plot(avg, error_bar = "se", order_by = "strength", to = "range_size") +
  ggplot2::coord_flip()
coef_plot(avg, error_bar = "se", order_by = "strength", to = "ss") +
  ggplot2::coord_flip()
###############################################
#harsh abundance
#abundance
newdata_harsh_ab<- subset(newdata_harsh, !(abundance %in% NA))
check<-name.check(newtree_global,newdata_harsh_ab)
tips_pruned<-check$tree_not_data
newtree_harsh_ab<-drop.tip(newtree_global,tips_pruned)
#log transformed
newdata_harsh_ab$log_ab<-log(newdata_harsh_ab$abundance+1)
#PGLS
model_harsh_ab<-phylolm(scale(log_ab)~social_system+scale(pre)+scale(pre_var_among)+scale(pre_var_within)+scale(tmp)+
                          scale(str)+scale(dtr)+scale(body_mass)+scale(range_size),data=newdata_harsh_ab,phy=newtree_harsh_ab,model="lambda",lower.bound=1e-15)
summary(model_harsh_ab)
vif.phyloglm(model_harsh_ab)
#AIC model average
dd<-MuMIn::dredge(model_harsh_ab)
bb<-MuMIn::model.avg(dd)
summary(bb)
#phylopath (check direct or indirect effect, n=2256)
newdata_harsh_ab$ss<-as.factor(newdata_harsh_ab$social_system)
#to avoid error, we need to standardize range size manually, other factors will be standardized by phylopath
newdata_harsh_ab$rs_std<-scale(newdata_harsh_ab$range_size)
#phylopath model
positions <- data.frame(
  name = c("tmp","pre_var_within","pre","pre_var_among","str","dtr" ,"ss", "rs_std","log_ab"),
  x = c(1:3,5:7, 4, 3.2,4.8),
  y = c(4,4,4,4,4,4,3, 1, 1)
)
m2 <- define_model_set(
  null=c(),
  one=c(rs_std~ss),
  two=c(log_ab~ss),
  three=c(log_ab~ss,rs_std~ss),
  four=c(log_ab~rs_std,rs_std~ss),
  five=c(log_ab~ss,rs_std~log_ab),
  .common=c(ss~pre+pre_var_among+tmp+dtr,
            rs_std~pre+pre_var_among+pre_var_within+tmp+str,
            log_ab~pre_var_among+tmp+str+dtr)
)
plot_model_set(m2, manual_layout = positions, edge_width = 0.5)
p <- phylo_path(m2, newdata_harsh_ab, newtree_harsh_ab,model="lambda")
s<-summary(p)
plot(s)

avg <- average(p,cut_off=2 ,avg_method="conditional")
plot(avg, algorithm = 'mds',manual_layout = positions)
coef_plot(avg, error_bar = "se", order_by = "strength", to = "log_ab") +
  ggplot2::coord_flip()
coef_plot(avg, error_bar = "se", order_by = "strength", to = "rs_std") +
  ggplot2::coord_flip()
######################################
#subset certain clade (benign p<0.25), n=1786
newdata_benign<- subset(newdata_global, (Clade %in% c("Bucerotidae","M6","P2","Psittacidae2","S2","CC4","CC5CC6","EurylaimidaePittidae",
                                                      "M5","P21","Paleognathae","Picidae","S10","S3","S9")))
check<-name.check(newtree_global,newdata_benign)
tips_pruned<-check$tree_not_data
newtree_benign<-drop.tip(newtree_global,tips_pruned)
#PGLS
model<-phylolm(scale(range_size)~social_system+scale(pre)+scale(pre_var_among)+scale(pre_var_within)+scale(tmp)+
                 scale(str)+scale(dtr)+scale(body_mass),data=newdata_benign,phy=newtree_benign,model="lambda",lower.bound=1e-20)
summary(model)
vif.phyloglm(model)
#AIC model average
dd<-MuMIn::dredge(model)
bb<-MuMIn::model.avg(dd)
summary(bb)
#check climate and ss
model_ss<-phyloglm(social_system~scale(pre)+scale(pre_var_among)+scale(pre_var_within)+scale(tmp)+
                     scale(dtr)+scale(str)+scale(body_mass),phy=newtree_benign,data=newdata_benign,
                   method="logistic_MPLE",btol=30)
summary(model_ss)
vif.phyloglm(model_ss)
#social_system
newdata_benign$pre_std<-scale(newdata_benign$pre)
newdata_benign$among_std<-scale(newdata_benign$pre_var_among)
newdata_benign$within_std<-scale(newdata_benign$pre_var_within)
newdata_benign$tmp_std<-scale(newdata_benign$tmp)
newdata_benign$str_std<-scale(newdata_benign$str)
newdata_benign$dtr_std<-scale(newdata_benign$dtr)
newdata_benign$body_mass_std<-scale(newdata_benign$body_mass)

var_list<-c("pre_std","among_std","within_std","tmp_std","str_std","dtr_std","body_mass_std")

find_all_cb<-function(var_list){
  xx<-seq(1,length(var_list))
  findcb<-function(x){
    all.comb<-combn(var_list,x)
    xy.list <- split(t(all.comb), seq(ncol(all.comb)))
    names(xy.list)<-paste(x,seq(1,length(xy.list)),sep="-")
    return(xy.list)
  }
  return(do.call(c,lapply(xx,findcb)))
}

nullmodel<-list(1)
names(nullmodel)<-"0-1"
qq<-find_all_cb(var_list)

f_hb<-function(x){
  model_coop_hb<-phyloglm(social_system~.,newdata_benign[,c("social_system",as.vector(unlist(x)))],newtree_benign,method="logistic_MPLE",btol=30)
  #return(summary(model_coop_hb))
  mAIC<-AIC(model_coop_hb)
  mAICc<-mAIC+(2*(length(unlist(x))+1)^2+2*(length(unlist(x))+1))/(nrow(newdata_benign)-(1+length(unlist(x)))-1)
  return(mAICc)
}

model_null<-phyloglm(social_system~1,newdata_benign,newtree_benign,method="logistic_MPLE",btol=30)
AICc_null<-AIC(model_null)+(2*1^2+2*1)/(nrow(newdata_benign)-1-1)
names(AICc_null)<-"Null"
model_name_null<-as.vector("Null")
names(model_name_null)<-"Null"

aiclist_hb<-rapply(qq,f_hb)
aiclist_hb<-c(aiclist_hb,AICc_null)
modellist_hb<-rapply(qq,paste,collapse="+")
modellist_hb<-c(modellist_hb,model_name_null)

hbaic<-data.frame(rank=seq(1,length(aiclist_hb)),
                  model=unlist(lapply(names(sort(aiclist_hb)),function(x){modellist_hb[names(modellist_hb)==x]})),
                  AICc=sort(aiclist_hb))
hbaic$dAICc<-hbaic$AICc-min(hbaic$AICc)
hbaic$Weight<-exp(-0.5*hbaic$dAICc)/sum(exp(-0.5*hbaic$dAICc))
hbaic$Accuw<-NA
for(i in 1:length(hbaic$Weight)){hbaic$Accuw[i]<-sum(hbaic$Weight[1:i])}
hbaic

f_avg<-function(x1,Cand.mods){
  estimate=modavg(cand.set = Cand.mods,parm=x1)$Mod.avg.beta
  se=modavg(cand.set = Cand.mods,parm=x1)$Uncond.SE
  z=estimate/se
  p=2*pnorm(-abs(z))
  out<-data.frame(Predictor=x1,Estimate=estimate,SE=se,Z=z,P=p)
  return(out)
}

#only include the model which dAICc<2
fm1<-phyloglm(social_system~among_std+dtr_std,newdata_benign,newtree_benign,method="logistic_MPLE",btol=30)
fm2<-phyloglm(social_system~among_std+within_std+str_std+dtr_std,newdata_benign,newtree_benign,method="logistic_MPLE",btol=30)
fm3<-phyloglm(social_system~among_std+within_std+dtr_std,newdata_benign,newtree_benign,method="logistic_MPLE",btol=30)
fm4<-phyloglm(social_system~among_std+dtr_std,newdata_benign,newtree_benign,method="logistic_MPLE",btol=30)
Cand.mods <- list("fm1" = fm1, "fm2" = fm2, "fm3" = fm3, "fm4" = fm4)

f_avg("(Intercept)",Cand.mods)
f_avg("among_std",Cand.mods)
f_avg("within_std",Cand.mods)
f_avg("dtr_std",Cand.mods)
f_avg("str_std",Cand.mods)
#N=1786, phylopath
newdata_benign$ss<-as.factor(newdata_benign$social_system)
#define model set
m <- define_model_set(
  null=c(),
  one=c(range_size~ss),
  .common=c(ss~pre_var_among+dtr,range_size~pre+pre_var_among+tmp+dtr+str+body_mass)
)
positions <- data.frame(
  name = c("tmp","pre","pre_var_among","str","dtr","body_mass" ,"ss", "range_size"),
  x = c(1:6, 3.5, 3.5),
  y = c(3,3,3,3,3,3, 2, 1)
)
plot_model_set(m, manual_layout = positions, edge_width = 0.5)
p <- phylo_path(m, newdata_benign, newtree_benign,model="lambda")
s<-summary(p)
plot(s)

avg <- average(p,cut_off=2 ,avg_method="conditional")
plot(avg, algorithm = 'mds',manual_layout = positions)
coef_plot(avg, error_bar = "se", order_by = "strength", to = "range_size") +
  ggplot2::coord_flip()
coef_plot(avg, error_bar = "se", order_by = "strength", to = "ss") +
  ggplot2::coord_flip()
###############################################
#benign abundance
#abundance
newdata_benign_ab<- subset(newdata_benign, !(abundance %in% NA))
check<-name.check(newtree_global,newdata_benign_ab)
tips_pruned<-check$tree_not_data
newtree_benign_ab<-drop.tip(newtree_global,tips_pruned)
#log transformed
newdata_benign_ab$log_ab<-log(newdata_benign_ab$abundance+1)
#PGLS
model_benign_ab<-phylolm(scale(log_ab)~social_system+scale(pre)+scale(pre_var_among)+scale(pre_var_within)+scale(tmp)+
                           scale(str)+scale(dtr)+scale(body_mass)+scale(range_size),data=newdata_benign_ab,phy=newtree_benign_ab,model="lambda",lower.bound=1e-15)
summary(model_benign_ab)
vif.phyloglm(model_benign_ab)
#AIC model average
dd<-MuMIn::dredge(model_benign_ab)
bb<-MuMIn::model.avg(dd)
summary(bb)
#N=1663, phylopath (check direct or indirect effect)
newdata_benign_ab$ss<-as.factor(newdata_benign_ab$social_system)
#to avoid error, we need to standardize range size manually, other factors will be standardized by phylopath
newdata_benign_ab$rs_std<-scale(newdata_benign_ab$range_size)
positions <- data.frame(
  name = c("tmp","pre_var_within","pre","pre_var_among","str","dtr","body_mass" ,"ss", "rs_std","log_ab"),
  x = c(1:7, 4, 3,5),
  y = c(4,4,4,4,4,4,4,3, 1, 1)
)
m2 <- define_model_set(
  null=c(),
  one=c(rs_std~ss),
  two=c(log_ab~ss),
  three=c(log_ab~ss,rs_std~ss),
  four=c(log_ab~rs_std,rs_std~ss),
  five=c(log_ab~ss,rs_std~log_ab),
  .common=c(ss~pre_var_among+dtr,
            rs_std~pre+pre_var_among+tmp+dtr+str+body_mass,
            log_ab~pre+pre_var_among+pre_var_within+tmp+dtr+str)
)
plot_model_set(m2, manual_layout = positions, edge_width = 0.5)
p <- phylo_path(m2, newdata_benign_ab, newtree_benign_ab,model="lambda")
s<-summary(p)
plot(s)

avg <- average(p,cut_off=2 ,avg_method="conditional")
plot(avg, algorithm = 'mds',manual_layout = positions)
coef_plot(avg, error_bar = "se", order_by = "strength", to = "log_ab") +
  ggplot2::coord_flip()
coef_plot(avg, error_bar = "se", order_by = "strength", to = "rs_std") +
  ggplot2::coord_flip()

###########################################
#global n=6553
#PGLS
model<-phylolm(scale(range_size)~social_system+scale(pre)+scale(pre_var_among)+scale(pre_var_within)+scale(tmp)+
                 scale(str)+scale(dtr)+scale(body_mass),data=newdata_global,phy=newtree_global,model="lambda",lower.bound=1e-15)
summary(model)
vif.phyloglm(model)
#AIC model average
dd<-MuMIn::dredge(model)
bb<-MuMIn::model.avg(dd)
summary(bb)
#check climate and ss
model_ss<-phyloglm(social_system~scale(pre)+scale(pre_var_among)+scale(pre_var_within)+scale(tmp)+
                     scale(dtr)+scale(str)+scale(body_mass),phy=newtree_global,data=newdata_global,
                   method="logistic_MPLE",btol=30)
summary(model_ss)
vif.phyloglm(model_ss)
#social_system
newdata_global$pre_std<-scale(newdata_global$pre)
newdata_global$among_std<-scale(newdata_global$pre_var_among)
newdata_global$within_std<-scale(newdata_global$pre_var_within)
newdata_global$tmp_std<-scale(newdata_global$tmp)
newdata_global$str_std<-scale(newdata_global$str)
newdata_global$dtr_std<-scale(newdata_global$dtr)
newdata_global$body_mass_std<-scale(newdata_global$body_mass)

var_list<-c("pre_std","among_std","within_std","tmp_std","str_std","dtr_std","body_mass_std")

find_all_cb<-function(var_list){
  xx<-seq(1,length(var_list))
  findcb<-function(x){
    all.comb<-combn(var_list,x)
    xy.list <- split(t(all.comb), seq(ncol(all.comb)))
    names(xy.list)<-paste(x,seq(1,length(xy.list)),sep="-")
    return(xy.list)
  }
  return(do.call(c,lapply(xx,findcb)))
}

nullmodel<-list(1)
names(nullmodel)<-"0-1"
qq<-find_all_cb(var_list)

f_hb<-function(x){
  model_coop_hb<-phyloglm(social_system~.,newdata_global[,c("social_system",as.vector(unlist(x)))],newtree_global,method="logistic_MPLE",btol=30)
  #return(summary(model_coop_hb))
  mAIC<-AIC(model_coop_hb)
  mAICc<-mAIC+(2*(length(unlist(x))+1)^2+2*(length(unlist(x))+1))/(nrow(newdata_global)-(1+length(unlist(x)))-1)
  return(mAICc)
}

model_null<-phyloglm(social_system~1,newdata_global,newtree_global,method="logistic_MPLE",btol=30)
AICc_null<-AIC(model_null)+(2*1^2+2*1)/(nrow(newdata_global)-1-1)
names(AICc_null)<-"Null"
model_name_null<-as.vector("Null")
names(model_name_null)<-"Null"

aiclist_hb<-rapply(qq,f_hb)
aiclist_hb<-c(aiclist_hb,AICc_null)
modellist_hb<-rapply(qq,paste,collapse="+")
modellist_hb<-c(modellist_hb,model_name_null)

hbaic<-data.frame(rank=seq(1,length(aiclist_hb)),
                  model=unlist(lapply(names(sort(aiclist_hb)),function(x){modellist_hb[names(modellist_hb)==x]})),
                  AICc=sort(aiclist_hb))
hbaic$dAICc<-hbaic$AICc-min(hbaic$AICc)
hbaic$Weight<-exp(-0.5*hbaic$dAICc)/sum(exp(-0.5*hbaic$dAICc))
hbaic$Accuw<-NA
for(i in 1:length(hbaic$Weight)){hbaic$Accuw[i]<-sum(hbaic$Weight[1:i])}
hbaic

f_avg<-function(x1,Cand.mods){
  estimate=modavg(cand.set = Cand.mods,parm=x1)$Mod.avg.beta
  se=modavg(cand.set = Cand.mods,parm=x1)$Uncond.SE
  z=estimate/se
  p=2*pnorm(-abs(z))
  out<-data.frame(Predictor=x1,Estimate=estimate,SE=se,Z=z,P=p)
  return(out)
}

#only include the model which dAICc<2
fm1<-phyloglm(social_system~pre_std+among_std+within_std+tmp_std+str_std,newdata_global,newtree_global,method="logistic_MPLE",btol=30)
fm2<-phyloglm(social_system~pre_std+among_std+within_std+tmp_std+body_mass_std,newdata_global,newtree_global,method="logistic_MPLE",btol=30)
Cand.mods <- list("fm1" = fm1, "fm2" = fm2)

f_avg("(Intercept)",Cand.mods)
f_avg("pre_std",Cand.mods)
f_avg("among_std",Cand.mods)
f_avg("within_std",Cand.mods)
f_avg("tmp_std",Cand.mods)
f_avg("str_std",Cand.mods)
f_avg("body_mass_std",Cand.mods)
##########################################
#N=6553, phylopath
newdata_global$ss<-as.factor(newdata_global$social_system)
#define model set
m <- define_model_set(
  null=c(),
  one=c(range_size~ss),
  .common=c(ss~pre+pre_var_among+tmp,range_size~pre+pre_var_among+pre_var_within+tmp+dtr+str)
)
positions <- data.frame(
  name = c("tmp","pre_var_within","pre","pre_var_among","str","dtr" ,"ss", "range_size"),
  x = c(1:3,5:7, 4, 4),
  y = c(3,3,3,3,3,3, 2, 1)
)
plot_model_set(m, manual_layout = positions, edge_width = 0.5)
p <- phylo_path(m, newdata_global, newtree_global,model="lambda")
s<-summary(p)
plot(s)

avg <- average(p,cut_off=2 ,avg_method="conditional")
plot(avg, algorithm = 'mds',manual_layout = positions)
coef_plot(avg, error_bar = "se", order_by = "strength", to = "range_size") +
  ggplot2::coord_flip()
coef_plot(avg, error_bar = "se", order_by = "strength", to = "ss") +
  ggplot2::coord_flip()
############################################
#abundance
newdata_global_ab<- subset(newdata_global, !(abundance %in% NA))
check<-name.check(newtree_global,newdata_global_ab)
tips_pruned<-check$tree_not_data
newtree_global_ab<-drop.tip(newtree_global,tips_pruned)
#log transformed
newdata_global_ab$log_ab<-log(newdata_global_ab$abundance+1)
#PGLS
model_global_ab<-phylolm(scale(log_ab)~social_system+scale(pre)+scale(pre_var_among)+scale(pre_var_within)+scale(tmp)+
                           scale(str)+scale(dtr)+scale(body_mass)+scale(range_size),data=newdata_global_ab,phy=newtree_global_ab,model="lambda",lower.bound=1e-15)
summary(model_global_ab)
vif.phyloglm(model_global_ab)
#AIC model average
dd<-MuMIn::dredge(model_global_ab)
bb<-MuMIn::model.avg(dd)
summary(bb)
######################################
#N=6129, phylopath (check direct or indirect effect)
newdata_global_ab$ss<-as.factor(newdata_global_ab$social_system)
#to avoid error, we need to standardize range size manually, other factors will be standardized by phylopath
newdata_global_ab$rs_std<-scale(newdata_global_ab$range_size)
positions <- data.frame(
  name = c("tmp","pre_var_within","pre","pre_var_among","str","dtr" ,"ss", "rs_std","log_ab"),
  x = c(1:3,5:7, 4, 3.5,4.5),
  y = c(4,4,4,4,4,4,3, 1, 1)
)

m2 <- define_model_set(
  null=c(),
  one=c(rs_std~ss),
  two=c(log_ab~ss),
  three=c(log_ab~ss,rs_std~ss),
  four=c(log_ab~rs_std,rs_std~ss),
  five=c(log_ab~ss,rs_std~log_ab),
  .common=c(ss~pre+pre_var_among+tmp,
            rs_std~pre+pre_var_among+pre_var_within+tmp+dtr+str,
            log_ab~pre_var_among+pre_var_within+tmp+dtr+str)
)
plot_model_set(m2, manual_layout = positions, edge_width = 0.5)
p <- phylo_path(m2, newdata_global_ab, newtree_global_ab,model="lambda")
s<-summary(p)
plot(s)

avg <- average(p,cut_off=2 ,avg_method="conditional")
plot(avg, algorithm = 'mds',manual_layout = positions)
coef_plot(avg, error_bar = "se", order_by = "strength", to = "log_ab") +
  ggplot2::coord_flip()
coef_plot(avg, error_bar = "se", order_by = "strength", to = "rs_std") +
  ggplot2::coord_flip()
