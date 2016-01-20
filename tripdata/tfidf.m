% tfidf.m : 
function [w]=tfidf(x)
[m,n]=size(x);
idf=zeros(n,1);
ni=sum(x~=0)';ni=ni+(ni==0);max(ni)
idf=log(m./ni);
w=sparse(m,n);
for j=1:n,
    w(:,j)=idf(j)*x(:,j);
end

%w=x.*repmat(idf',m,1);