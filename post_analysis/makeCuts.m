function [data,sourceCoord,sources] = makeCuts(filename,catalogueName,degreesAwayFromCenter)

fid = fopen(filename);
mydata = textscan(fid, '%f %f %f %f %f %f %f %f %f %f %*[^\n]', 'delimiter', ',','CollectOutput',1);
data=mydata{1};
data=[data(:,1:5) data(:,10)];
fclose(fid);


%%%%%%%%%%%%
% This value is the amount of the galactic plane that will be removed.
% Therefore photons that have l abs (removeFromPlane) <  removed

% Value is in degrees.
removeFromPlane=5;
%%%%%%%%%%%%

[sourceCoord,sources] = readCat(catalogueName,1);

[rows,~]=size(sourceCoord);
i=1;
for j=1:rows
    if abs(sourceCoord(i,2))<removeFromPlane
        sourceCoord(i,:)=[];
        sources(i,:)=[];
        i=i-1;
        rows=rows-1;
    end
    i=i+1;
end

%At this point we have a list of sources that are not in the galactic plane

[rows,~]=size(sourceCoord);
[rowsData,colsData]=size(data);

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Now create the cuts!
% For each source, go through all the photons
for i=1:rows                %PARSE THE TEV SOURCES
    p=1;
    
    photonsAroundSource=zeros(1,colsData);
    angularDistance=zeros(1,1);
   for j=1:rowsData         %PARSE THE PHOTONS
       
       % Find distance between each photon and the source center
       % Use cos(A) = sin(Decl.1)sin(Decl.2) + cos(Decl.1)cos(Decl.2)cos(RA.1 - RA.2) and thus, A = arccos(A)
       % Only use (l,b) instead of (RA,DEC)
       
       angularDistance_temp = angDist(data(j,4:5),sourceCoord(i,1:2));      
       
       if(angularDistance_temp<=degreesAwayFromCenter)
            photonsAroundSource(p,:) = data(j,:);
            angularDistance(p,1)=angularDistance_temp;
            p=p+1;
            
        end
   end

   loc = strcat('data/', sources{i},'.mat');
   sourceName =sources{i};
   
   sourceCoordinates=sourceCoord(i,1:2);
   save(loc,'photonsAroundSource','sourceName','sourceCoordinates','angularDistance');
   clearvars photonsAroundSource angularDistance;
   
end
sources =strtrim(sources);
loc = strcat('allData','.mat');
save(loc,'data','sourceCoord','sources');
% Problems:
% Rough cut isnt working, its letting in too many photons
% Also, data is only 5 columns. Its coded this way at the begining of this
% file. Not a big deal to fix.



% ^^
% Fixed it.
% Problem was that the values were not in Aitoff projection.
% However, new caviate is that my Aitoff goes from -180 to 180 deg, whereas ds9 Aitoff is from 180 to 360 then 0 to 180.





end

