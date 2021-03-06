clear
%makeCuts('lat_final_10GeV_alldata.txt','tevcat2.reg',2);
load('allData');
[rows,cols]=size(sourceCoord);
[rowsData,colsData]=size(data);

% 1: Normal Aitoff Projection
% 2: Aitoff Projection of Photon Cuts
% 3: Spectrums
input=3;
numberOfBins=20;


r=5;

if input==1
    figure
    hold on
    
    aitoff_coord=zeros(rowsData,2);
    for i=1:rowsData
        aitoff_coord(i,:) = aitoff(data(i,4:5)); 
 
    end
    plot(aitoff_coord(:,1),aitoff_coord(:,2),'b.') ; 

    aitoff_sourceCoord=zeros(rows,2);
    for i=1:rows
       aitoff_sourceCoord(i,:)=aitoff(sourceCoord(i,1:2)); 
       endx
    
    plot(aitoff_sourceCoord(:,1),aitoff_sourceCoord(:,2),'r.') ; 

    set(gca,'FontSize',16);                
    saveas(gca,'graphs/Aitoff Projection','epsc2');
    end
end
if input==2
    figure
    hold on
    
    for i=1:rows
        loc=['/home/james/fermidata/spectra/data/',sources{i},'.mat'];
        load(loc);
        [rows_p,~]=size(photonsAroundSource);

        temp1=aitoff(sourceCoordinates);
        for j=1:rows_p
            temp2(j,:)=aitoff(photonsAroundSource(j,4:5));    
        end    
        plot(temp2(:,1),temp2(:,2),'.');
        plot(temp1(1),temp1(2),'r.');
    end
    set(gca,'FontSize',16);                
    saveas(gca,'graphs/Cut Aitoff Projection','epsc2');
end

if input==3
    figure
    set(gcf,'Visible', 'off');
   
    for i=1:rows
        loc=['/home/james/fermidata/spectra/data/',sources{i},'.mat'];
        load(loc);
        
        [rows_p,~]=size(photonsAroundSource);
        energy=zeros(rows_p,1);
        angularDistance=zeros(rows_p,1);
        
        for j=1:rows_p
            energy(j,1) = photonsAroundSource(j,1);
            angularDistance(j,1) = angDist(photonsAroundSource(j,4:5),sourceCoordinates);     
            
        end
              
        [photonsInBin,binCenters]=hist(angularDistance,numberOfBins);
        g=1/sqrt(2*pi)*exp(-0.5*binCenters.^2);
        figure
        bar(binCenters,photonsInBin/trapz(binCenters,photonsInBin));hold on
        plot(binCenters,g,'r');hold off
        
        set(gca,'FontSize',16);            
        xlabel('Normalized Angular Distance ({\circ})','FontSize',16);
        ylabel('Number of Photons','FontSize',16);
        title(sources{i});
        saveas(gca,['graphs/',sources{i},'_NORMALIZEDHISTOGRAM'],'epsc2');
        
        figure
        
        hist(angularDistance,numberOfBins);
        set(gca,'FontSize',16);
        xlabel('Angular Distance ({\circ})','FontSize',16);
        ylabel('Number of Photons','FontSize',16);
        title(sources{i});
        saveas(gca,['graphs/',sources{i},'_HISTOGRAM'],'epsc2');
    end

    set(gcf,'Visible', 'on');
end


%     set(gca,'FontSize',16);                
%     xlabel('','FontSize',16);
%     ylabel('Number of Photons','FontSize',16);
%     saveas(gca,,'eps');

