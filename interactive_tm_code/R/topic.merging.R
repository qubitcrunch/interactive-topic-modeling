topic.merging<-function(topic_matrix,topic_likelihoods, anchor_groups,weighted_merge=TRUE){

out<-do.call("cbind",lapply(anchor_groups,function(group){

if(weighted_merge){
M<-match(group,colnames(topic_matrix))
weights<-topic_likelihoods[M]/sum(topic_likelihoods[M])
out_col<-apply(topic_matrix[,group],1,function(x)sum(x* weights))
}
else{
out_col<-rowMeans(topic_matrix[,group])
}
out_col
}))

out_topic_likelihoods	<-	unlist(lapply(anchor_groups,function(group){
M<-match(group,colnames(topic_matrix))
sum(topic_likelihoods[M])
}))


out_topic_likelihoods <-	out_topic_likelihoods/sum(out_topic_likelihoods)
colnames(out)<-unlist(lapply(anchor_groups,function(group)paste(group,collapse=",")))

list(topic_matrix=out,topic_likelihoods= out_topic_likelihoods)
}
