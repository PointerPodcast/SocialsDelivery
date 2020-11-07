import 'dart:convert';
import 'dart:core';
import 'dart:typed_data';
//import 'dart:html' as html;
import 'package:http/http.dart' as http;
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:table_calendar/table_calendar.dart';
import 'package:flutter_time_picker_spinner/flutter_time_picker_spinner.dart';
import 'package:file_picker/file_picker.dart';
import 'package:flutter_beautiful_popup/main.dart';
import 'package:flutter_beautiful_popup/templates/Fail.dart';
import 'package:flutter_beautiful_popup/templates/GreenRocket.dart';
import './constants.dart';
import './PlusMinusCounter.dart';

void main() {
  runApp(MyApp());
}

class MyApp extends StatelessWidget {
  // This widget is the root of your application.
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'SocialDelivery',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        brightness: Brightness.dark,
        
      ),
      home: MyHomePage(title: 'SocialDelivery'),
    );
  }
}

class MyHomePage extends StatefulWidget {
  MyHomePage({Key key, this.title}) : super(key: key);


  final String title;

  @override
  _MyHomePageState createState() => _MyHomePageState();
}

class _MyHomePageState extends State<MyHomePage> {
    
    static final String ip = Constants.ip;
    static final String port = Constants.port;

    final String auth_url = "http://$ip:$port/socialdelivery/api/v1.0/authenticate";
    final String deploy_url = "http://$ip:$port/socialdelivery/api/v1.0/deliverepisode";
    final String get_cover_url = "http://$ip:$port/socialdelivery/api/v1.0/getcover/";
    final String delete_url = "http://$ip:$port/socialdelivery/api/v1.0/deleteepisode";

    String FLI_fieldName = "Facebook/Instagram/Linkedin Post";
    static final FLI_fix_maxLenght = 700-55;
    int FLI_maxLenght = FLI_fix_maxLenght;
    int FLI_MaxLines = 7;
    TextEditingController FLI_controller = new TextEditingController();

    String Twitter_fieldName = "Twitter Post";
    static final Twitter_fix_maxLenght = 280-55;
    int Twitter_maxLenght = Twitter_fix_maxLenght;
    int Twitter_maxLines = 7;
    TextEditingController Twitter_controller = new TextEditingController();

    String titleFieldName = "Episode Title";
    int titleMaxLenght = 100;
    int titleMaxLines = 1;
    TextEditingController titleController = new TextEditingController();

    String episodeNumberFieldName = "Episode Number";
    int episodeNumberMaxLenght = 4;
    int episodeNumberMaxLines = 1;
    TextEditingController episodeNumberController = new TextEditingController();

    String episodeNumberGetCoverFieldName = "Episode Number";
    int episodeNumberGetCoverMaxLenght = 4;
    int episodeNumberGetCoverMaxLines = 1;
    TextEditingController episodeNumberGetCoverController = new TextEditingController();

    String episodeNumberDeleteName = "Episode Number";
    int episodeNumberDeleteLenght = 4;
    int episodeNumberDeleteMaxLines = 1;
    TextEditingController episodeNumberDeleteController = new TextEditingController();
    
    String passwordFieldName = "Password";
    int passwordMaxLenght = 20;
    int passwordMaxLines = 1;
    TextEditingController passwordController = new TextEditingController();

    String passwordDeleteFieldName = "Password";
    int passwordDeleteMaxLenght = 20;
    int passwordDeleteMaxLines = 1;
    TextEditingController passwordDeleteController = new TextEditingController();

    CalendarController _calendarController = CalendarController();

    List<GuestSocials> guests = new List();

    bool somethingIsEmpty = true;

    DateTime _dateTime = DateTime.now();

    PlatformFile platformFile;
    Image image;
    FilePickerResult result;

    Image imageCover;

    void initState() {
        super.initState();
        _calendarController = CalendarController();
    }

    @override
    void dispose() {
      _calendarController.dispose();
      super.dispose();
    }

    Future getImage() async {
        final FilePickerResult _result = await FilePicker.platform.pickFiles(type: FileType.image);
        setState(() {
          if (_result != null) {
            result = _result;
            platformFile = result.files.first;
            image = Image.memory(platformFile.bytes);
          } else {
            print('No image selected.');
          }
        });
      }

    Future discardImage() async{
        setState(() {
            result = null;
            platformFile = null;
            image = null;
        });
    }

    void _addGuest(){
        TextEditingController nameSurnameController = new TextEditingController();
        TextEditingController facebookController = new TextEditingController();
        TextEditingController instagramController = new TextEditingController();
        TextEditingController twitterController = new TextEditingController();
        TextEditingController linkedinController = new TextEditingController();
        TextEditingController telegramController = new TextEditingController();

        GuestSocials guest = new GuestSocials(
                nameSurnameController: nameSurnameController,
                facebookController: facebookController,
                instagramController: instagramController,
                twitterController: twitterController,
                linkedinController: linkedinController,
                telegramController: telegramController,
        );
        setState(() {
            guests.add(guest);
        });
    }

    void _removeGuest(){
        if (guests.length > 0){
            setState(() {
                guests.removeLast();
            });
        }
    }

    void setSomethingIsEmpty(bool val){
        setState(() {
            this.somethingIsEmpty = val;
        });
    }

    void updateMaxChars(){
        String id = "Pointer["+episodeNumberController.text+"] ";
        String title = titleController.text;
        int charCount = (id+title).length;
        setState(() {
            FLI_maxLenght = FLI_fix_maxLenght - charCount;
            Twitter_maxLenght = Twitter_fix_maxLenght - charCount;
        });
    }


    Future<http.Response> postAuth(String password){
        return http.post(
                auth_url,
                headers: <String, String>{
                    'Content-Type': 'application/json; charset=UTF-8',
                },
                body: jsonEncode(<String, String>{
                    'password' : password,
                }),
        );
    }

    Future<http.Response> postDelivery(Map infoMapper){
        return http.post(
                deploy_url,
                headers: <String, String>{
                    'Content-Type': 'application/json; charset=UTF-8',
                },
                body: jsonEncode(<String, dynamic>{
                    'episode_number': infoMapper['episode_number'],
                    'title' : infoMapper['title'],
                    'fli_post' : infoMapper['fli_post'],
                    'twitter_post' : infoMapper['twitter_post'],
                    'guests_number' : infoMapper['guests_number'],
                    'guests' : jsonEncode(infoMapper['guests']),
                    'password' : infoMapper['password'],
                    'date' : infoMapper['date'],
                    'time' : infoMapper['time'],
                    'custom_cover_name' : infoMapper['custom_cover_name'],
                    'custom_cover_data' : infoMapper['custom_cover_data'],
                }),
        );
    }

    Future<http.Response> postDelete(String episodeNumber, String password){
        return http.post(
                delete_url,
                headers: <String, String>{
                    'Content-Type': 'application/json; charset=UTF-8',
                },
                body: jsonEncode(<String, String>{
                    'episode_number' : episodeNumber,
                    'password' : password,
                }),
        );
    }


    showPopupOK(context, String title, String content){
        final popupOk = BeautifulPopup(
                context: context,
                template: TemplateGreenRocket,
                );
        popupOk.show(
                title: title,
                content: content,
                actions: [
                    popupOk.button(
                        label: 'Close',
                        onPressed: Navigator.of(context).pop,
                    )
                ],
        );
    }

    showPopupFail(context, String title, String content){
        final popupOk = BeautifulPopup(context: context, template: TemplateFail);
        popupOk.show(
                title: title,
                content: content,
                actions: [
                    popupOk.button(
                        label: 'Close',
                        onPressed: Navigator.of(context).pop,
                    )
                ],
        );
    }


    Map inputFormatter(){ 
        Map infoMapper = new Map();

        //AddNumber if not empty
        String episodeNumber = episodeNumberController.text.trim();
        infoMapper['episode_number'] = episodeNumber;

        //AddTitle if not empty
        String title = titleController.text.trim();
        infoMapper['title'] = title;

        String fliPost = FLI_controller.text.trim();
        infoMapper['fli_post'] = fliPost;

        String twitterPost = Twitter_controller.text.trim();
        infoMapper['twitter_post'] = twitterPost;

        int day = _calendarController.selectedDay.day;
        int month = _calendarController.selectedDay.month;
        int year = _calendarController.selectedDay.year;
        String date = "$day-$month-$year";
        print("DATE: $date");
        infoMapper['date'] = date;
        
        int hour = _dateTime.hour;
        int minute = _dateTime.minute;
        String time = "$hour:$minute";
        print("TIME: $time");
        infoMapper['time'] = time;


        int guestsNumber = guests.length;
        infoMapper['guests_number'] = guestsNumber;

        //Check if custom_cover has been uploaded
        image == null ? infoMapper['custom_cover'] = false : infoMapper['custom_cover'] = true;

        String password = passwordController.text.trim();
        print("Password: $password");
        infoMapper['password'] = password;

        if ( episodeNumber.isEmpty || title.isEmpty || fliPost.isEmpty || twitterPost.isEmpty || date.isEmpty || time.isEmpty || password.isEmpty){
                showPopupFail(context, "Missing Values", "Check that each field has been filled");
                return infoMapper = null;
        }

        int id = 0;
        Map<String,Map<String,String>> guestsToId = new Map();
        for (GuestSocials g in guests){
            Map<String,String> socialsTag = new Map();

            String realName = g.nameSurnameController.text.trim();
            if(realName.isEmpty){
                showPopupFail(context, "Missing Real Name", "Please fill the field");
                return infoMapper = null;
            }

            String facebook = g.facebookController.text.trim();

            String instagram = g.instagramController.text.trim();

            String linkedin = g.linkedinController.text.trim();

            String twitter = g.twitterController.text.trim();

            String telegram = g.telegramController.text.trim();

            if( realName.isEmpty || facebook.isEmpty || instagram.isEmpty || linkedin.isEmpty || twitter.isEmpty || telegram.isEmpty){
                //TODO: lanciare un popup "Sei sicuro di voler continuare"
            }

            if(facebook.isEmpty)
                facebook = "#";
            if(instagram.isEmpty)
                instagram = "#";
            if (linkedin.isEmpty)
                linkedin = "#";
            if(twitter.isEmpty)
                twitter = "#";
            if(telegram.isEmpty)
                telegram = "#";

            socialsTag['real_name'] = realName;
            socialsTag['facebook'] = facebook;
            socialsTag['instagram'] = instagram;
            socialsTag['linkedin'] = linkedin;
            socialsTag['twitter'] = twitter;
            socialsTag['telegram'] = telegram;

            guestsToId['$id'] = socialsTag;
            id++;
        }
        infoMapper['guests'] = guestsToId;
        return infoMapper;
    }

    void deleteEpisode(context, String episodeNumber, String password) async{
        http.Response deleteResponse = await postDelete(episodeNumber, password);
        var resData = jsonDecode(deleteResponse.body)['message'];
        bool resultData = resData['result'];
        String status = resData['status'];
        if (resultData)
            showPopupOK(context, "OK!", status);
        else
            showPopupFail(context, "Not Deleted", status);
    }

    void getCover(context, String episodeNumber) async{
        print(get_cover_url+episodeNumber);
        http.Response getCoverResponse = await http.get(
                get_cover_url+episodeNumber,
                headers: <String, String>{
                    'Content-Type': 'application/json; charset=UTF-8',
                });
        Uint8List imageByteArray = getCoverResponse.bodyBytes;
        setState(() {
            imageCover = Image.memory(imageByteArray);
        });
    }

    void deliveryButton(context) async{
        Map infoMapper = inputFormatter();
        if(infoMapper == null)
            return;
        http.Response authResponse = await postAuth(infoMapper['password']);
        Map decoded = jsonDecode(authResponse.body);
        bool authIsOk = decoded['message']['result'];
        http.Response deliveryResponse;
        if( authIsOk ){
            if(result != null){
                    infoMapper['custom_cover_name'] = platformFile.name;
                    infoMapper['custom_cover_data'] = platformFile.bytes;
            }
            deliveryResponse = await postDelivery(infoMapper);
            var resData = jsonDecode(deliveryResponse.body)['message'];
            bool resultData = resData['result'];
            String status = resData['status'];
            if(resultData == true)
                showPopupOK(context, "Posts are on the way!", "Delivered Pointer[${infoMapper['episodeNumber']}]!");
            else
                showPopupFail(context, "NOT DELIVERED", status);
        }else{
            showPopupFail(context, "Failed Authentication", decoded['message']['status']);
        }
    }




    Widget getTimePickerSpinner() {
      return new TimePickerSpinner(
        is24HourMode: true,
        normalTextStyle: TextStyle(
          fontSize: 24,
          color: Colors.white,
        ),
        highlightedTextStyle: TextStyle(
          fontSize: 24,
          color: Colors.pinkAccent,
          fontWeight: FontWeight.bold,
        ),
        spacing: 50,
        itemHeight: 80,
        isForce2Digits: true,
        onTimeChange: (time) {
          setState(() {
            _dateTime = time;
          });
        },
      );
    }

    @override
    Widget build(BuildContext context) {
        return Scaffold(
                appBar: AppBar(
                        centerTitle: true,
                        title: Text(
                                widget.title,
                                style: TextStyle(
                                        color: Colors.pink,
                                        fontSize: 40,
                                        fontWeight: FontWeight.bold,
                                ),
                        ),
                ),
                body: SingleChildScrollView(
                        child: Column(
                                children: <Widget>[
                                    Center(
                                        child: Row(
                                            children: [
                                                Flexible(
                                                        flex: 4,
                                                        child:  Padding(
                                                            padding: EdgeInsets.all(50),
                                                            child: SocialDeliveryTextField(
                                                                fieldName: episodeNumberFieldName,
                                                                maxLength: episodeNumberMaxLenght,
                                                                maxLines: episodeNumberMaxLines,
                                                                border: false,
                                                                onlyNumber: true,
                                                                controller: episodeNumberController,
                                                                onEditingComplete: (){
                                                                    updateMaxChars();
                                                                    if (episodeNumberController.text.isEmpty)
                                                                        setSomethingIsEmpty(true);
                                                                    else
                                                                        setSomethingIsEmpty(false);
                                                                }
                                                            ),
                                                        ),
                                                ),
                                                Expanded(
                                                        flex: 5,
                                                        child:  Padding(
                                                            padding: EdgeInsets.all(50),
                                                            child: SocialDeliveryTextField(
                                                                fieldName: titleFieldName,
                                                                maxLength: titleMaxLenght,
                                                                maxLines: titleMaxLines,
                                                                border: false,
                                                                controller: titleController,
                                                                onEditingComplete: (){
                                                                    updateMaxChars();
                                                                    if (titleController.text.isEmpty)
                                                                        setSomethingIsEmpty(true);
                                                                    else
                                                                        setSomethingIsEmpty(false);
                                                                }
                                                            ),
                                                        ),
                                                ),
                                            ],
                                        ),
                                    ),
                                    Row(
                                            children: [
                                                Expanded(
                                                        flex: 5,
                                                        child: Padding(
                                                            padding: EdgeInsets.all(20),
                                                            child: SocialDeliveryTextField(
                                                                fieldName: FLI_fieldName,
                                                                maxLength: FLI_maxLenght,
                                                                maxLines: FLI_MaxLines,
                                                                border: true,
                                                                controller: FLI_controller,
                                                                onEditingComplete: (){
                                                                    if (FLI_controller.text.isEmpty)
                                                                        setSomethingIsEmpty(true);
                                                                    else
                                                                        setSomethingIsEmpty(false);
                                                                }
                                                            ),
                                                        ),
                                                ),
                                                Expanded(
                                                        flex: 5,
                                                        child: Padding(
                                                            padding: EdgeInsets.all(20),
                                                            child: SocialDeliveryTextField(
                                                                fieldName: Twitter_fieldName,
                                                                maxLength: Twitter_maxLenght,
                                                                maxLines: Twitter_maxLines,
                                                                border: true,
                                                                controller: Twitter_controller,
                                                                onEditingComplete: (){
                                                                    if (Twitter_controller.text.isEmpty)
                                                                        setSomethingIsEmpty(true);
                                                                    else
                                                                        setSomethingIsEmpty(false);
                                                                }
                                                            ),
                                                        ),
                                                ),
                                            ]
                                    ),
                                    Container(
                                            height: 2,
                                            width: double.infinity,
                                            color: Colors.pinkAccent
                                    ),
                                    Container(
                                                   child: Table(
                                                        children :[
                                                            TableRow(
                                                                    children: [
                                                                        Padding(
                                                                            padding: EdgeInsets.all(20),
                                                                            child: Text("Name Surname",
                                                                                textAlign: TextAlign.center,
                                                                                style: TextStyle(
                                                                                        fontSize: 15,
                                                                                        fontWeight: FontWeight.bold,
                                                                                )
                                                                            ),
                                                                        ),
                                                                        Padding(
                                                                            padding: EdgeInsets.all(20),
                                                                            child: Text("Facebook",
                                                                                textAlign: TextAlign.center,
                                                                                style: TextStyle(
                                                                                        fontSize: 15,
                                                                                        fontWeight: FontWeight.bold,
                                                                                )
                                                                            ),
                                                                        ),
                                                                        Padding(
                                                                            padding: EdgeInsets.all(20),
                                                                            child: Text("Instagram",
                                                                                textAlign: TextAlign.center,
                                                                                style: TextStyle(
                                                                                        fontSize: 15,
                                                                                        fontWeight: FontWeight.bold,
                                                                                )
                                                                            ),
                                                                        ),
                                                                        Padding(
                                                                            padding: EdgeInsets.all(20),
                                                                            child:Text("Twitter",
                                                                                textAlign: TextAlign.center,
                                                                                style: TextStyle(
                                                                                        fontSize: 15,
                                                                                        fontWeight: FontWeight.bold,
                                                                                )
                                                                            ),
                                                                        ),
                                                                        Padding(
                                                                            padding: EdgeInsets.all(20),
                                                                            child: Text("Linkedin",
                                                                                textAlign: TextAlign.center,
                                                                                style: TextStyle(
                                                                                        fontSize: 15,
                                                                                        fontWeight: FontWeight.bold,
                                                                                ),
                                                                            ),
                                                                        ),
                                                                        Padding(
                                                                            padding: EdgeInsets.all(20),
                                                                            child: Text("Telegram",
                                                                                textAlign: TextAlign.center,
                                                                                style: TextStyle(
                                                                                        fontSize: 15,
                                                                                        fontWeight: FontWeight.bold,
                                                                                ),
                                                                            ),
                                                                        ),
                                                                    ]
                                                            ),
                                                        ]
                                                ),
                                    ),
                                    for( GuestSocials g in guests) g,
                                    Container(
                                            height: 2,
                                            width: double.infinity,
                                            color: Colors.grey,
                                    ),
                                    Padding(
                                        padding: EdgeInsets.all(40),
                                        child: PlusMinusCounter(
                                                addGuest: _addGuest,
                                                removeGuest: _removeGuest,
                                        ),
                                    ),
                                    Container(
                                            height: 2,
                                            width: double.infinity,
                                            color: Colors.pinkAccent
                                    ),

                                    Row(
                                            mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                                            children: [
                                                Flexible(
                                                        flex: 5,
                                                        child: Column(
                                                            children: [
                                                                    Padding(
                                                                        padding: EdgeInsets.all(20),
                                                                        child: Text("Delivery Date",
                                                                           textAlign: TextAlign.center,
                                                                           style: TextStyle(
                                                                                   color: Colors.greenAccent,
                                                                                   fontSize: 30,
                                                                                   fontWeight: FontWeight.bold,
                                                                           ),
                                                                        ),
                                                                    ),
                                                                    Container(
                                                                        width: 500,
                                                                        height: 500,
                                                                        child: TableCalendar(
                                                                            calendarController: _calendarController,
                                                                        ),
                                                                    ),
                                                            ]
                                                        ),
                                                ),
                                                VerticalDivider(),
                                                Flexible(
                                                        flex: 3,
                                                        child: Column(
                                                                children: [
                                                                    Text("Delivery Time",
                                                                       textAlign: TextAlign.center,
                                                                       style: TextStyle(
                                                                               color: Colors.greenAccent,
                                                                               fontSize: 30,
                                                                               fontWeight: FontWeight.bold,
                                                                       ),
                                                                    ),
                                                                    getTimePickerSpinner(),
                                                                ],
                                                        ),
                                                ),
                                            ]
                                    ),
                                    Container(
                                            height: 2,
                                            width: double.infinity,
                                            color: Colors.pinkAccent
                                    ),
                                    Column(
                                        mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                                        children: [
                                            Padding(
                                                padding: EdgeInsets.all(30),
                                                child: Container(
                                                        height: image == null ? 30 : image.height,
                                                        child: Center(
                                                            child: image == null
                                                                ? Text('No image selected.')
                                                                : image,
                                                          ),
                                                        ),
                                            ),
                                            Row(
                                                mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                                                    children: [
                                                        Padding(
                                                            padding: EdgeInsets.all(20),
                                                            child: RaisedButton(
                                                                    textColor: Colors.white,
                                                                    color : Colors.green,
                                                                    onPressed: getImage,
                                                                    child: Text("Upload Custom Cover",
                                                                                   style: TextStyle(
                                                                                           fontSize: 20,
                                                                                   )
                                                                            ),
                                                                ),
                                                        ),
                                                        Padding(
                                                            padding: EdgeInsets.all(20),
                                                            child: RaisedButton(
                                                                    textColor: Colors.white,
                                                                    color : Colors.red,
                                                                    onPressed: discardImage,
                                                                    child: Text("Discard Upload Cover",
                                                                                   style: TextStyle(
                                                                                           fontSize: 20,
                                                                                   )
                                                                            ),
                                                                ),
                                                        ),
                                                        ]
                                                    ),
                                        ]
                                    ),
                                    Container(
                                            height: 2,
                                            width: double.infinity,
                                            color: Colors.pinkAccent
                                    ),
                                    Row(
                                            mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                                            children: [
                                                Flexible(
                                                        flex: 1,
                                                        child: Container(
                                                            width: 300,
                                                            child: Padding(
                                                                padding: EdgeInsets.all(50),
                                                                child: SocialDeliveryTextField(
                                                                    fieldName: passwordFieldName,
                                                                    maxLength: passwordMaxLenght,
                                                                    maxLines: passwordMaxLines,
                                                                    border: false,
                                                                    onlyNumber: false,
                                                                    controller: passwordController,
                                                                    onEditingComplete: (){
                                                                        if (passwordController.text.isEmpty)
                                                                            setSomethingIsEmpty(true);
                                                                        else
                                                                            setSomethingIsEmpty(false);
                                                                    }
                                                                ),
                                                            ),
                                                        ),
                                                ),
                                                Center(
                                                    child: RaisedButton(
                                                        textColor: Colors.white,
                                                        color : Colors.pinkAccent,
                                                        onPressed: () => deliveryButton(context),
                                                        child: Text("Deliver!",
                                                                       style: TextStyle(
                                                                               fontSize: 30,
                                                                               fontWeight: FontWeight.bold,
                                                                       )
                                                                ),
                                                    ),
                                                ),
                                            ]
                                    ),
                                    Container(
                                            height: 10,
                                            width: double.infinity,
                                            color: Colors.blueAccent
                                    ),
                                    Column(
                                        mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                                        children: [
                                            Padding(
                                                padding: EdgeInsets.all(30),
                                                child: Container(
                                                            child: Text("Get Cover of Episode N°",
                                                               textAlign: TextAlign.center,
                                                               style: TextStyle(
                                                                       color: Colors.greenAccent,
                                                                       fontSize: 30,
                                                                       fontWeight: FontWeight.bold,
                                                               ),
                                                            ),
                                                ),
                                            ),
                                            Padding(
                                                padding: EdgeInsets.all(30),
                                                child: Container(
                                                        height: imageCover == null ? 30 : imageCover.height,
                                                        child: Center(
                                                            child:  imageCover == null
                                                                ? Text('No image selected.')
                                                                : imageCover,
                                                          ),
                                                        ),
                                            ),
                                            Row(
                                                mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                                                    children: [
                                                            Flexible(
                                                                    flex: 4,
                                                                    child:  Padding(
                                                                        padding: EdgeInsets.all(50),
                                                                        child: SocialDeliveryTextField(
                                                                            fieldName: episodeNumberGetCoverFieldName,
                                                                            maxLength: episodeNumberGetCoverMaxLenght,
                                                                            maxLines: episodeNumberGetCoverMaxLines,
                                                                            border: false,
                                                                            onlyNumber: true,
                                                                            controller: episodeNumberGetCoverController,
                                                                            onEditingComplete: (){
                                                                                if (episodeNumberGetCoverController.text.isEmpty)
                                                                                    setSomethingIsEmpty(true);
                                                                                else
                                                                                    setSomethingIsEmpty(false);
                                                                            }
                                                                        ),
                                                                    ),
                                                            ),
                                                            Padding(
                                                                padding: EdgeInsets.all(20),
                                                                child: RaisedButton(
                                                                        textColor: Colors.white,
                                                                        color : Colors.blueAccent,
                                                                        onPressed: () => getCover(context, episodeNumberGetCoverController.text),
                                                                        child: Text("Get Cover",
                                                                                       style: TextStyle(
                                                                                               fontSize: 20,
                                                                                       )
                                                                                ),
                                                                    ),
                                                            ),
                                                        ]
                                                    ),
                                        ]
                                    ),
                                    Container(
                                            height: 10,
                                            width: double.infinity,
                                            color: Colors.redAccent
                                    ),

                                    Column(
                                        mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                                        children: [
                                            Padding(
                                                padding: EdgeInsets.all(30),
                                                child: Container(
                                                            child: Text("Delete Episode / Unschedule",
                                                               textAlign: TextAlign.center,
                                                               style: TextStyle(
                                                                       color: Colors.greenAccent,
                                                                       fontSize: 30,
                                                                       fontWeight: FontWeight.bold,
                                                               ),
                                                            ),
                                                ),
                                            ),
                                        ]
                                    ),
                                    Row(
                                        mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                                            children: [
                                                    Flexible(
                                                            flex: 1,
                                                            child:  Padding(
                                                                padding: EdgeInsets.all(50),
                                                                child: SocialDeliveryTextField(
                                                                    fieldName: episodeNumberDeleteName,
                                                                    maxLength: episodeNumberDeleteLenght,
                                                                    maxLines: episodeNumberDeleteMaxLines,
                                                                    border: false,
                                                                    onlyNumber: true,
                                                                    controller: episodeNumberDeleteController,
                                                                    onEditingComplete: (){
                                                                        if (episodeNumberDeleteController.text.isEmpty)
                                                                            setSomethingIsEmpty(true);
                                                                        else
                                                                            setSomethingIsEmpty(false);
                                                                    }
                                                                ),
                                                            ),
                                                    ),
                                                    Flexible(
                                                            flex: 2,
                                                            child: Container(
                                                                width: 300,
                                                                child: Padding(
                                                                    padding: EdgeInsets.all(50),
                                                                    child: SocialDeliveryTextField(
                                                                        fieldName: passwordDeleteFieldName,
                                                                        maxLength: passwordDeleteMaxLenght,
                                                                        maxLines: passwordMaxLines,
                                                                        border: false,
                                                                        onlyNumber: false,
                                                                        controller: passwordDeleteController,
                                                                        onEditingComplete: (){
                                                                            if (passwordDeleteController.text.isEmpty)
                                                                                setSomethingIsEmpty(true);
                                                                            else
                                                                                setSomethingIsEmpty(false);
                                                                        }
                                                                    ),
                                                                ),
                                                            ),
                                                    ),
                                                    Padding(
                                                        padding: EdgeInsets.all(20),
                                                        child: RaisedButton(
                                                                textColor: Colors.white,
                                                                color : Colors.redAccent,
                                                                onPressed: () => deleteEpisode(context, episodeNumberDeleteController.text, passwordDeleteController.text),
                                                                child: Text("Delete Episode",
                                                                               style: TextStyle(
                                                                                       fontSize: 20,
                                                                               )
                                                                        ),
                                                            ),
                                                    ),
                                                ]
                                            ),
                                ],
                        ),
                    ),
        );
    }
}

class GuestSocials extends StatefulWidget{

    final TextEditingController nameSurnameController;
    final TextEditingController facebookController;
    final TextEditingController instagramController;
    final TextEditingController twitterController;
    final TextEditingController linkedinController;
    final TextEditingController telegramController;

    const GuestSocials({
        Key key,
        @required this.nameSurnameController,
        @required this.facebookController,
        @required this.instagramController,
        @required this.twitterController,
        @required this.linkedinController,
        @required this.telegramController,
    }) : super(key: key);

    @override
    _GuestSocialsState createState() => _GuestSocialsState();
}

class _GuestSocialsState extends State<GuestSocials>{

    @override
    Widget build(BuildContext context){
           return Table(
                children :[
                    TableRow(
                            children: [
                                Padding(
                                    padding: EdgeInsets.all(20),
                                    child: TextFormField(
                                            textAlign: TextAlign.center,
                                            controller : widget.nameSurnameController,
                                    ),
                                ),
                                Padding(
                                    padding: EdgeInsets.all(20),
                                    child: TextFormField(
                                            textAlign: TextAlign.center,
                                            controller : widget.facebookController,
                                    ),
                                ),
                                Padding(
                                    padding: EdgeInsets.all(20),
                                    child: TextFormField(
                                            textAlign: TextAlign.center,
                                            controller : widget.instagramController,
                                    ),
                                ),
                                Padding(
                                    padding: EdgeInsets.all(20),
                                    child: TextFormField(
                                            textAlign: TextAlign.center,
                                            controller : widget.twitterController,
                                    ),
                                ),
                                Padding(
                                    padding: EdgeInsets.all(20),
                                    child: TextFormField(
                                            textAlign: TextAlign.center,
                                            controller : widget.linkedinController,
                                    ),
                                ),
                                Padding(
                                    padding: EdgeInsets.all(20),
                                    child: TextFormField(
                                            textAlign: TextAlign.center,
                                            controller : widget.telegramController,
                                    ),
                                ),
                            ]
                    ),
                ]
        );
    }
}

class SocialDeliveryTextField extends StatefulWidget{

    final String fieldName;
    final TextEditingController controller;
    final Function onEditingComplete;
    int maxLength;
    int maxLines;
    bool border;
    bool onlyNumber;

    SocialDeliveryTextField({
        Key key, 
        @required this.fieldName,
        @required this.controller,
        @required this.onEditingComplete,
        this.maxLength = 700,
        this.maxLines = 1,
        this.border = true,
        this.onlyNumber = false,
    }) : super(key: key);

    @override
    _SocialDeliveryTextFieldState createState() => _SocialDeliveryTextFieldState();

}

class _SocialDeliveryTextFieldState extends State<SocialDeliveryTextField>{


    @override
    Widget build(BuildContext context){
        return Container(
                width: MediaQuery.of(context).size.width/2,
                child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: <Widget>[
                            Text(
                                    widget.fieldName,
                                    style: TextStyle(
                                            color: Colors.white,
                                            fontSize: 20,
                                            fontWeight: FontWeight.bold,
                                    ),
                            ),
                            TextFormField(
                                    maxLength: widget.maxLength,
                                    controller: widget.controller,
                                    onEditingComplete: widget.onEditingComplete,
                                    decoration: InputDecoration(
                                            isDense: true,
                                            border:  widget.border ?
                                            OutlineInputBorder(
                                                    borderSide: BorderSide(color: Colors.black)
                                            )
                                            : null
                                    ),
                                    inputFormatters: widget.onlyNumber ?
                                        <TextInputFormatter>[
                                            FilteringTextInputFormatter.digitsOnly,
                                        ] 
                                        : null,
                                    maxLines: widget.maxLines,
                            ),
                        ],
                ),
        );
    }

}
