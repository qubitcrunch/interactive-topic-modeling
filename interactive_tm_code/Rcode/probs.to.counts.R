prob.to.counts	<-	function(bow,topic_matrix,topic_likelihoods){
								
								constant	<-	sum(unlist(lapply(bow,ncol)))
								topic_sums	<-	as.matrix(as.integer(round(unname(topic_likelihoods* constant))))
								topic_counts	<-	t(sapply(1:ncol(topic_matrix),function(j){
														this_topic			<-	as.integer(round(topic_matrix[,j]* topic_sums[j,]))
														this_topic
														}))
								colnames(topic_counts)	<-	rownames(topic_matrix)
								rownames(topic_counts)	<-	colnames(topic_matrix)
								return(list(topic_matrix= topic_counts,topic_sums= topic_sums))
								}
