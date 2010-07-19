/**
 test for a threshold from TF-IDF data, and 
 generate plots to visualize the threshold effect

 author: Paco Nathan <ceteri@gmail.com>
 */

data <- read.csv("thresh.tsv", sep='\t', header=F)
t_data <- data[,3]
print(summary(t_data))

# pass through values for 80+ percentile
qntile <- .8
t_thresh <- quantile(t_data, qntile)

# CDF plot
title <- "CDF threshold max(tfidf)"
xtitle <- paste("thresh:", t_thresh)
par(mfrow=c(2, 1))
plot(ecdf(t_data), xlab=xtitle, main=title)
abline(v=t_thresh, col="red")
abline(h=qtile, col="yellow")

# box-and-whiskers plot
boxplot(t_data, horizontal=TRUE)
rug(t_data, side=1)
