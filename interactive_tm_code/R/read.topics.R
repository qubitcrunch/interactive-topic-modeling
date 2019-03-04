get.topics	<- function(filepath, vocab, K, V) {
	A	<-	matrix(0, nrow=K, ncol=V)
	con	<-	file(filepath, "r")
	k	<-	0
	i	<-	1
	while ( TRUE ) {
		line <- readLines(con, n = 1)
		#print(line)
		if ( length(line) == 0 ) {
			break
		}
		if(line==""||line=="--------------"||line=="------------------------"||line=="\n"){
			i	<-	1
		}
		else if(length(grep("Topic", line))>0){
			k	<-	k+1
		}
		else{
			x 			<- strsplit(line, "\t")[[1]]
			val			<-	as.numeric(x[1])
			word			<-	x[2]
			index		<-	match(word, vocab)
			A[k, index]	<-	val
		}	
	}
  close(con)
  A	<-	t(apply(A, 1, function(x) x/sum(x)))
  return(A)
}

syn.data.file 	<- commandArgs(trailingOnly=TRUE)[1]
topic.in.file	<- commandArgs(trailingOnly=TRUE)[2]
topic.out.file	<- commandArgs(trailingOnly=TRUE)[3]

load(syn.data.file)
K	<-	nrow(phis)
V	<-	ncol(phis)

A <- get.topics(topic.in.file, effective.vocab, K, V)

write.table(A, file=topic.out.file)
