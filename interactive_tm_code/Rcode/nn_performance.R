nn_performance<-function(lines_in, labels_in,topic_object,num_samples,thetas_in=FALSE){

if(!thetas_in){
cat("lexicalizing ... ")
vocab<-rownames(topic_object$topic_matrix)
cat
docs<-lexicalize(lines_in,vocab=vocab)

cat("converting probs to counts ... ","\n")
counts<-prob.to.counts(docs, topic_object$topic_matrix, topic_object $topic_likelihoods)

cat("running inference ... ","\n")
out<-infer.topics(docs,topic_counts=counts$topic_matrix,topic_sums=counts$topic_sums,alpha=ncol(topic_object$topic_matrix)/20,eta=.01,n_iters=50)
thetas<- t(out$document_sums) / colSums(out$document_sums)
cat(dim(thetas),"\n")
non_nas<-which(!is.na(rowSums(thetas)))
cat(length(non_nas),"\n")
labels<-labels_in[non_nas]
thetas<-thetas[non_nas,]
}else{
	if(is.null(topic_object)){
		stop("Need a file with infered documents!")
		}else{
			cat("loading thetas ...","\n")
			
			thetas	<-	as.matrix(read.table(topic_object))
			cat(dim(thetas))
			labels	<-	labels_in
		}	
	}

samples<-sample(nrow(thetas),num_samples)
thetas_s<-thetas[samples,]
labels_s<-labels[samples]

cat("running nearest neighborts ... ","\n")
accuracy<-do.call("rbind",lapply(1:nrow(thetas_s),function(i){

cat(i,"\n")
l1_dist<-apply(thetas_s[-i,],1,function(l)sum(abs(l-thetas_s[i,])))
sapply(c(10,20,50,100,200),function(num_nns)sum(labels_s[order(l1_dist,decreasing=FALSE)[1:num_nns]]%in%labels_s[i])/num_nns)
}))

colMeans(accuracy)
}

