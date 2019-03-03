require(RJSONIO)
require(tm)
require(stringr)

args            <- commandArgs(trailingOnly=TRUE)
dataset			<- args[1]
this_dir        <- args[2]
out_dir			<- args[3]

remove.words		<-	function(str, stopwords) {
  						x <- unlist(strsplit(str, " "))
  						paste(x[!x %in% stopwords], collapse = " ")
						}

years 			<-	as.character(c(2009:2018))

docs		<-	lapply(years,function(year){
					
				lines_in		<-	readLines(paste0(this_dir,"/",year,"_full_docs.jsonl"),encoding="UTF-8")
				cat(paste("Processing", length(lines_in),"articles from", year),"\n")
				docs		<-	sapply(1:length(lines_in),function(l){
				this_list	<-	try(fromJSON(lines_in[l]),silent=TRUE)
				if(class(class(this_list))!="try-error"){
					out			<-	lapply(this_list,function(el){
									this_l	<-	tolower(str_replace_all(el, "[^[:alnum:]]", " "))
									this_l	<-	str_replace_all(this_l, "[[0,1,2,3,4,5,6,7,8,9]]", " ")
									this_l	<-	str_trim(this_l,side="both")
									this_l	<-	sapply(this_l,function(x)stemDocument(stripWhitespace(remove.words(x,stopwords("SMART")))),USE.NAMES=FALSE)
								})

						unlist(unname(out[which.max(unname(unlist(
						lapply(out,function(l){
							if(class(l)=="character"){
								length(strsplit(l," ")[[1]])
									}else{
									0
							}
						})
					)))]))
					}
			})	

	})

cat("Getting vocabulary and converting to uci sparse format","\n")

###save for tdm 
all_lines	<-	do.call("c",docs)
dates		<-	unlist(sapply(1:length(years),function(i)rep(years[i],length(docs[[i]]))))
tm			<-	Corpus(VectorSource(all_lines))


#build tdm
tdm				<-	TermDocumentMatrix(tm)
#word_wants		<-	which(row_sums(tdm)>thresh)
#doc_wants		<-	which(col_sums(tdm)>thresh)
#all_lines		<-	all_lines[doc_wants]
#dates			<-	dates[doc_wants]
#tdm				<-	tdm[word_wants, doc_wants]
vocab			<-	rownames(tdm)
D 				<-	nrow(t(tdm))
cat(paste("Total number of articles:",D),"\n")
W   				<-	ncol(t(tdm))
cat(paste("Total number of words:",W),"\n")
N				<-	sum(t(tdm))
triplet_mat		<-	cbind(t(tdm)$i,t(tdm)$j,t(tdm)$v)

write.table(triplet_mat,file=paste0(out_dir,"/",dataset,".txt"),quote=FALSE,row.names=FALSE,col.names=FALSE)
file_conn	<-	file(paste0(out_dir,"/",dataset,".txt"),"r+")
writeLines(c(as.character(D),as.character(W),as.character(N)),file_conn)
close(file_conn)
lines		<-	readLines(paste0(out_dir,"/",dataset,".txt"))[-4]
write.table(lines,file=paste0(out_dir,"/",dataset,".txt"),quote=FALSE,row.names=FALSE,col.names=FALSE)
write.table(vocab,file=paste0(out_dir,"/","vocab.",dataset,".txt"),quote=FALSE,row.names=FALSE,col.names=FALSE)

