require(stringr)
lund.topics	<-	function(dtm_txt_file,loss){
	
						system(paste("cd py_code && /usr/bin/python learn_topics_facets.py","settings.example",paste0("../data_uci/",str_replace(dtm_txt_file,".txt",""),".mat.trunc.mat"),loss))

								A				<-	read.table("py_code_output/result_.A_facets")
								#C				<-	read.table("anchor-word-tools/tmp/result_.C")
								topic_liks		<-	read.table("py_code_output/result_.topic_likelihoods_facets")
								
																		   return(list(topic_matrix=A,topic_likelihoods=topic_liks))
	
}
