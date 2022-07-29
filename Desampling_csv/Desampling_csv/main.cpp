#include <iostream>
#include <fstream>
#include <string>

#define OVERSAMPLINGRATE 20

using namespace std;

int main()
{
    string orgin_path;
    string target_path;
    string inter;
    fstream origin;
    fstream target;
    long double accumulator=0;
    char str[150];

    int desamplingrate = 1;
    int i = 0,j=1;
    cout << "please input a full path of csv file" << endl;

    while(cin.getline(str,149)) {
        orgin_path = str;
        if (orgin_path.empty()) {
            continue;
        }

        origin.open(orgin_path.c_str(), ios::in);

        if (!origin) {
            cout << "file not exist" << endl;
            continue;
        }
        cout << orgin_path << endl;
        cout << "file open success" << endl;

        cout << "please input desampling rate" << endl;
        cin >> desamplingrate;

        target_path = orgin_path.insert(orgin_path.length()-4,"_desampled");
        target.open(orgin_path.c_str(), ios::out);

        orgin_path = "";
        target_path = "";

        while(!origin.eof()) {
            origin.getline(str,149);
            inter = str;
            accumulator = accumulator + atof(inter.c_str());
            if((i%desamplingrate) == 0) {
                //target<<inter;
                accumulator = accumulator/desamplingrate;
                if(i==0) {
                    target<<inter;
                }else{
                    target<<accumulator;
                }
                target<<","<<endl;
                accumulator = 0;
                cout << j << "line" << endl;
                j++;
            }

            if(i < desamplingrate) {
                i++;
            }else {
                i=1;
            }
        }

        accumulator = 0;
        origin.close();
        target.close();
        j=0;
        cout << "please input a full path of csv file" << endl;
    }

    return 0;
}
