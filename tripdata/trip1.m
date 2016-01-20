% trip1.m
%ind=find(full(sum(A)>2));
%At=A(:,ind);
%np=tfidf(normsen(A'));
%np=norm1x(tfidf((A')));
%np=norm1x(A');
np=tfidf(A');
dict=dictionary;
[n,m]=size(np);
rand('state',0);
k=10
[W,H]=nmf(np,rand(n,k),rand(k,m),.0000005,100,10000);
%[W,H]=nmf_alsobs(np,k,10,1);
[val,ind]=max(H);
H=H';
eH=entp(H);
% extracting top words and top reviews, saving results 
fp=fopen('trip1_10.txt','wt');
fprintf(fp,'Summary %d X %d into %d Topics\n\n', n,m,k);
for i=1:k,
    [valg,indg]=sort(H(:,i),'descend');
    gind=find(ind==i);
    hw=entp(H(gind,:));
    sw=sum(H(gind,:)');sw1=sw+(sw==0);
    rw=mean(valg(gind)'./sw1);
    fprintf(fp,'\n\nTopic %d concepts   Total posts # %d   Average Post Entropy %f   Max weight portion %f\n \n',i,length(gind),mean(hw),rw);
    dict(indg(1:12),:)
      fprintf(fp,'%s\n\n',dict(indg(1:12),:)');

     [valg,indg]=sort(W(:,i),'descend');
%    [valg,indg]=sort(W(:,i).*(max(pscore-nscore,0))','descend');
    for j=1:10,
        dstr=dict(find(A(:,indg(j))),:);
        [md,nd]=size(dstr);
      fprintf(fp,'Topic %d, Sentence %d, tweet %d, %s\n', i,j,indg(j),reshape(dstr',1,md*nd));
%titles{indg(j)}(2,:)
%      fprintf(fp,'Topic %d, Sentence %d, tweet %d, %s\n', i,j,indg(j),titles{indg(j)}(2,:));
    end  
%    fprintf(fp,'%s\n\n',dict(indg(1:12),:)');
%    [valg,indg]=sort(W(:,i).*sqrt(max(nscore-pscore,0))','descend');
%    for j=1:10,
 %     fprintf(fp,'Topic %d, Sentence %d,  %s\n', i,j,titles{indg(j)}(2,:));
  %  end  
    

  %  fprintf(fp,'Topic %d review title, date, rest name, location, type\n %s\n',i,words);
end
fclose(fp)
