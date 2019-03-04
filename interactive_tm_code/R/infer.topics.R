infer.topics	<-	function(bow,topic_counts,topic_sums,alpha,eta,n_iters,arora=TRUE){
						#Perform topic inference
						model		<-	lda.collapsed.gibbs.sampler(documents= bow,K=nrow(topic_counts),vocab=colnames(topic_counts) ,n_iters,alpha,eta, initial=list(topics=topic_counts,topic_sums=topic_sums), freeze.topics=TRUE,compute.log.likelihood=TRUE)
							
						return(model)
}
