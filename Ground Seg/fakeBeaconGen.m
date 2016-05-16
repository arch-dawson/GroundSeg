fid = fopen('ISS1m.txt','r');

format long

done = false;
count = 4;
data = cell(87841,2);
posVel = zeros(2,3);
h = waitbar(0,'Reading in data...');

while(~feof(fid))
    switch(mod(count,4))
        case 1
            C = strsplit(line);
        case 2 
            pos = strsplit(line);
            posVel(1,1) = str2double(pos{2});
            posVel(1,2) = str2double(pos{3});
            posVel(1,3) = str2double(pos{4});
        case 3 
            vel = strsplit(line);
            posVel(2,1) = str2double(vel{2});
            posVel(2,2) = str2double(vel{3});
            posVel(2,3) = str2double(vel{4});
        case 0
            data{count/4,1} = C{1};
            data{count/4,2} = posVel;
    end
    
    line = fgetl(fid);
    count = count + 1;
    waitbar((count/4)/87841)
end
data(1,:) = [];
fclose(fid);
close(h);

g = waitbar(0,'Writing data...');
posVelID = fopen('posVelData.txt','w');
for i = 1:87840
    fprintf(posVelID,'%s,%s,%s,%s,%s,%s,%s\n',data{i,1},num2hex(data{i,2}(1,1)),num2hex(data{i,2}(1,2)),num2hex(data{i,2}(1,3)),num2hex(data{i,2}(2,1)),num2hex(data{i,2}(2,2)),num2hex(data{i,2}(2,3)));
    waitbar(i/87841)
end
close(g);