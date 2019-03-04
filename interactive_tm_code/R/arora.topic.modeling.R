arora.topic.modeling	<-	function(dtm_txt_file,num_topics,loss,trunc_thresh,type="full",anchors=NULL){
								require(stringr)
								##Input:  doc term matrix file, voca text file, num topic, loss
								##Output: Topic matrix and topic likelihoods
						
					cat("tranforming data to scipy format","\n")
								system(paste("cd py_code && /usr/bin/python uci_to_scipy.py", paste0("../data_uci/",dtm_txt_file), paste0("../data_uci/",str_replace(dtm_txt_file,".txt",""),".mat")))
					
					cat("truncating vocab","\n")
								system(paste("cd py_code && /usr/bin/python truncate_vocabulary.py", paste0("../data_uci/",str_replace(dtm_txt_file,".txt",""),".mat"), paste0("../data_uci/vocab.",dtm_txt_file),trunc_thresh))
								
								vocab			<-	readLines(paste0("data_uci/","vocab.",dtm_txt_file,".trunc"))	
					
					cat("running arora","\n")
					if(type=="full"){
								system(paste("cd py_code && /usr/bin/python learn_topics.py",paste0("../data_uci/",str_replace(dtm_txt_file,".txt",""),".mat.trunc.mat"),"settings.example", paste0(" ../data_uci/vocab.",dtm_txt_file,".trunc"),num_topics,loss,"../py_code_output/result_"))
								}
					if(type=="partial"){
						if(is.null(anchors)){
							warning("anchors are missing")
							
						}else{
						write.table(anchors,file="py_code_output/anchorfile.txt",col.names=FALSE,row.names=FALSE,quote=FALSE)
						system(paste("cd py_code && /usr/bin/python learn_topics_partial.py",paste0("../data_uci/",str_replace(dtm_txt_file,".txt",""),".mat.trunc.mat"),"settings.example", paste0(" ../data_uci/vocab.",dtm_txt_file,".trunc"),length(anchors),loss,"../py_code_output/result_","../py_code_output/anchorfile.txt"))
						}
						
					}

								A				<-	read.table("py_code_output/result_.A")
								
								rownames(A)		<-	vocab
								
								#C				<-	read.table("anchor-word-tools/tmp/result_.C")
								topic_liks		<-	read.table("py_code_output/result_.topic_likelihoods")
								anchors			<-	read.table("py_code_output/result_.anchors")
								#Q_anchors		<-	read.table("py_code_output/result_.Q_anchors")
								
								#Q				<-	read.table("anchor-word-tools/tmp/result_.Q_mat")
														
						return(list(topic_matrix=A,topic_likelihoods=topic_liks,anchors=anchors))	
								
								}	

