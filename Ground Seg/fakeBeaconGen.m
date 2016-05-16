fid = fopen('ISSdata','r');

done = false;
count = 0;
data = {};

while(~feof(fid))
    switch(mod(count,4))
        case 1
            disp(line);
        case 2 
            pos = line; 
        case 3 
            vel = line;
        case 0
    end
    line = fgetl(fid);
    count = count + 1;
end