eqcoord=photonsAroundSource(:,2:3);
galcoord=photonsAroundSource(:,4:5);

[rows,~]=size(eqcoord);
angularDist=zeros(rows,2);
for i=1:rows
    
    % Self check if gal/eq makes a difference
    angularDist(i,1)=angDist(eqtogal(photonsAroundSource(i,2:3)),photonsAroundSource(i,4:5));
    angularDist(i,2)=angDist2(eqtogal(photonsAroundSource(i,2:3)),photonsAroundSource(i,4:5));
    
    % Ang Distance in gal and then eq USING DAVES FORMULA
    angularDist(i,3)=angDist(photonsAroundSource(1,4:5),photonsAroundSource(i,4:5));
    angularDist(i,4)=angDist(photonsAroundSource(1,2:3),photonsAroundSource(i,2:3));

    % Is rad the problem?
    angularDist(i,5)=angDistNORAD(photonsAroundSource(1,4:5),photonsAroundSource(i,4:5));
    angularDist(i,6)=angDistNORAD(photonsAroundSource(1,2:3),photonsAroundSource(i,2:3));

    
    
    
end
