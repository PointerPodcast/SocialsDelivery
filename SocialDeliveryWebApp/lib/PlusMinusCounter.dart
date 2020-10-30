import 'package:flutter/material.dart';

class PlusMinusCounter extends StatefulWidget {

    final Function addGuest;
    final Function removeGuest;

    const PlusMinusCounter({
        Key key,
        this.addGuest,
        this.removeGuest
    }) : super(key: key);

    @override
    _PlusMinusCounterState createState() => _PlusMinusCounterState();
}

class _PlusMinusCounterState extends State<PlusMinusCounter> {


    @override
    Widget build(BuildContext context) {
        return Container(
                child: new Center(
                        child: new Row(
                                mainAxisAlignment: MainAxisAlignment.start,
                                children: <Widget>[
                                    Padding(
                                        padding: EdgeInsets.all(10),
                                        child: Text(
                                            "Guest",
                                            style: TextStyle(
                                                    fontSize: 20,
                                            ),
                                        ),
                                    ),
                                    Padding(
                                        padding: EdgeInsets.all(10),
                                        child: FloatingActionButton(
                                            heroTag: "btn1",
                                            onPressed: minus,
                                            child: new Icon(
                                                    Icons.remove,
                                                    color: Colors.white
                                                    ),
                                            backgroundColor: Colors.red,
                                            ),
                                    ),
                                    Padding(
                                        padding: EdgeInsets.all(10),
                                        child: FloatingActionButton(
                                            heroTag: "btn2",
                                            onPressed: add,
                                            child: new Icon(
                                                    Icons.add,
                                                    color: Colors.white
                                                    ),
                                            backgroundColor: Colors.green,
                                            ),
                                    ),
                                ],
                        ),
                )
                        );
    }

    void add() {
        widget.addGuest();
    }

    void minus() {
        widget.removeGuest();
    }
}
