#include <iostream>
#include <opencv2/opencv.hpp>
#include <opencv2/highgui.hpp>

using std::cout;
using std::endl;

//hold 'q' while script is running to ensure frames are being iterated through
int main() {
    //initialize classifiers and capture
    cv::CascadeClassifier face_classifier = cv::CascadeClassifier("/Users/ashankbehara/GitHub/GotMask/Pure-OpenCV/HAAR Cascade/haarcascade_frontalface_default.xml");
    cv::CascadeClassifier mouth_classifier = cv::CascadeClassifier("/Users/ashankbehara/GitHub/GotMask/Pure-OpenCV/HAAR Cascade/haarcascade_mcs_mouth.xml");
    cv::VideoCapture capture(0);
    if  (!capture.isOpened()){
        cout << "Capture is not initialized" << endl;
    }

    //Real time object detection and classifications
    while (capture.isOpened()) {

        //Get color and grayscale frames
        cv::Mat color;
        capture >> color;
        cv::Mat frame;
        cv::cvtColor(color,frame,cv::COLOR_BGR2GRAY);

        //get bounding boxes
        std::vector<cv::Rect> faces,mouths;
        face_classifier.detectMultiScale(frame,faces, 1.3, 5);  
        mouth_classifier.detectMultiScale(frame, mouths,1.3,5);

        //unpack values from each face bounding box and draw bounding box of frontal face
        for (cv::Rect face: faces) {
            int x = face.x;
            int y = face.y;
            int h = face.height;
            int w = face.width;
            cv::Point topLeft(x,y);
            cv::Point bottomRight(x + w, y + h);
            cv::rectangle(color, topLeft, bottomRight, (127,0,255), 2);
            bool flag = false;
            
            //unpack values from mouth bounding box and check if contained inside frontal face box
            for (cv::Rect mouth : mouths){
                int mx = mouth.x;
                int my = mouth.y;
                int mh = mouth.height;
                int mw = mouth.width;
                if ((mx >= x && mx <= x + w) && (my >= y && my <= y + h) ) {
                    flag = true;  
                }
            }  

            // change text based on Region of Interest classification
            cv::Point origin(x,y-25);
            if (flag) {
                cv::putText(color, "Not Masked :(", origin, cv::FONT_HERSHEY_SIMPLEX, 1 ,(127,0,255), 2, cv::LINE_AA);
            } else {
                cv::putText(color, "Masked :)", origin, cv::FONT_HERSHEY_SIMPLEX, 1, (127,0,255), 2, cv::LINE_AA);
            }

        }

        //display colored frame with bounding box and classification text
        cv::imshow("Frame", color);

        //break when "enter" or "return" key is pressed
        if (cv::waitKey(0) == 13) {
            break;
        }
    }

    //delete, release, and destroy
    capture.release();
    cv::destroyAllWindows();
}