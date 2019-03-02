get.doc.topics	<- function(filepath, K=20, D=18723) {
	M	<-	matrix(0, nrow=D, ncol=K)
	con	<-	file(filepath, "r")
	while ( TRUE ) {
		line		<- readLines(con, n = 1)
		if ( length(line) == 0 ) {
			break
		}
		x 		<- strsplit(line, "\t")[[1]]
		doc		<- as.integer(tail(strsplit(x[2], "_")[[1]], n=1))

		split.list	<-	strsplit(x[3:length(x)], ":")
		topics		<-	sapply(split.list, function(ll) as.integer(ll[1]), USE.NAMES=FALSE)
		topics		<-	topics + 1
		props		<-	sapply(split.list, function(ll) as.integer(ll[2]), USE.NAMES=FALSE)
		props		<-	props/sum(props)

		doc.topics			<-	rep(0, K)
		doc.topics[topics]	<-	props
		
		M[doc,]	<-	doc.topics	
	}
	close(con)
	return(M)
}

in.file	<- commandArgs(trailingOnly=TRUE)[1]
out.file	<- commandArgs(trailingOnly=TRUE)[2]

M		 <- get.doc.topics(in.file)

write.table(M, file=out.file)
