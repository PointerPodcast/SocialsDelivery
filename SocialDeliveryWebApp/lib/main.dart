import 'dart:io';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:table_calendar/table_calendar.dart';
import 'package:flutter_time_picker_spinner/flutter_time_picker_spinner.dart';
import 'package:flutter_web_image_picker/flutter_web_image_picker.dart';
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
    String FLI_fieldName = "Facebook/Instagram/Linkedin Post";
    int FLI_maxLenght = 700;
    int FLI_MaxLines = 7;
    TextEditingController FLI_controller = new TextEditingController();

    String Twitter_fieldName = "Twitter Post";
    int Twitter_maxLenght = 280;
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
    
    String passwordFieldName = "Password";
    int passwordMaxLenght = 20;
    int passwordMaxLines = 1;
    TextEditingController passwordController = new TextEditingController();

    CalendarController _calendarController = CalendarController();

    List<GuestSocials> guests = new List();

    bool somethingIsEmpty = true;

    TextEditingController nameSurnameController = new TextEditingController();
    TextEditingController facebookController = new TextEditingController();
    TextEditingController instagramController = new TextEditingController();
    TextEditingController twitterController = new TextEditingController();
    TextEditingController linkedinController = new TextEditingController();

    DateTime _dateTime = DateTime.now();

    Image image;

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
        final _image = await FlutterWebImagePicker.getImage;
        setState(() {
          if (_image != null) {
            image = _image;
          } else {
            print('No image selected.');
          }
        });
      }

    void _addGuest(){
        TextEditingController nameSurnameController = new TextEditingController();
        TextEditingController facebookController = new TextEditingController();
        TextEditingController instagramController = new TextEditingController();
        TextEditingController twitterController = new TextEditingController();
        TextEditingController linkedinController = new TextEditingController();

        GuestSocials guest = new GuestSocials(
                nameSurnameController: nameSurnameController,
                facebookController: facebookController,
                instagramController: instagramController,
                twitterController: twitterController,
                linkedinController: linkedinController,
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

    void deliveryButton(){
        print(_calendarController.selectedDay);
        // Respond to button press
        //TODO: CHECK ALL FIELDS ARE VALID
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
                                            Padding(
                                                padding: EdgeInsets.all(30),
                                                child: RaisedButton(
                                                        textColor: Colors.white,
                                                        color : Colors.blueGrey,
                                                        onPressed: getImage,
                                                        child: Text("Upload Custom Cover",
                                                                       style: TextStyle(
                                                                               fontSize: 20,
                                                                       )
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
                                                        onPressed: deliveryButton,
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

    const GuestSocials({
        Key key,
        @required this.nameSurnameController,
        @required this.facebookController,
        @required this.instagramController,
        @required this.twitterController,
        @required this.linkedinController,
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
