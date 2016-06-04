
$(document).ready(function() {
    
    

    // Default variables
    var conn = null;                                    // global connection object
    var disconn = 0;                                    // checks if connection was closed by server or user
    var errorconn = 0;                                  // checks if connection is havving error
    var app_type = null;                                // type of search - what kind of app - e-commer, music, ticket, medical, food, social, video, image
    var disabled = true;                                // search box disabled or not
    var dis = 0;                                        // disabled on focus true or not
    var search = true;                                  // condition to search or not search, i.e start connection or not
    var connAgain = 0;                                  // flag to control should we connect afain after disconnecting
    var $sbox = $('.suggestion_row .list-group');       // the suggestion area

    // app code array for  app_type
    var app = {
                "Photo Sharing App": 'photo',
                "Video Sharing App": 'video',
                "Chat App": 'chat',
                "Medical App": 'medical',
                "Social Networking App": 'social',
                "Food App": 'food',
                "Music App": 'music',
                "E-Commerce App": 'commerce',
                "Movie/Event Tickets App": 'movie'    
    };                             


    
    $('.dropdown-menu li a').click(function(e) {
        console.log('insdie $(".dropdown-menu li a").click()');

        console.log('diabled : '+disabled+' dis : '+dis);

        e.preventDefault();

        app_type = $(this).text();

        console.log('search type : ', app_type);

        if (app_type === 'None')
        {
            app_type = "Select App Type";
            search = false;
            disabled = true;
        }
        else
        {
            var i = app_type.indexOf('Eg:');
            app_type = app_type.substring(0,i);
            disabled = false;
        }

        console.log('App type : ', app_type);

        $(this).closest('div').find('button[data-toggle="dropdown"]').html(app_type + ' <span class="caret"></span>');

        $(this).closest('div').toggleClass('open');

        $(this).closest('div').find('button[data-toggle="dropdown"]').attr('aria-expanded', false);
        
        if (search === true)
        {
            if (conn === null) {
                console.log('insdie conn === null');
            
                connect();
            } 
            // else 
            // {
            //     console.log('insdie conn !== null');
            
            //     disconnect();
            //     connAgain = 1;
            // }

        }
        

        console.log('returning from search_type.click()');

        console.log('RETURNING TIME -> diabled : '+disabled+' dis : '+dis);

        return false;
    });





    // Funciton called when user disconnects using Disconnect button
    function disconnect() {
        console.log('insdie diconnect()');
        
        if (conn !== null) {
            console.log('insdieconn !== null');
        
            disconn = 1;
            conn.close();
        }

        console.log('returning from diconnect()');
        
    }



    // function called when user clicks on connect button, initated by click event
    function connect() {
        console.log('insdie connect()');
        
        // first call disconnect() to be clean any stale previous connections
        disconnect();

        // // To add any other transport layers to be used if websocket is not possible
        // var transports = $('#protocols input:checked').map(function() {
        //     return $(this).attr('id');
        // }).get();

        // sockjs connection object created
        conn = new SockJS('http://' + window.location.host + '/sockjs_search');


        // Sockjs onOpen event triggered when connection is opened and readystate is OPEN
        conn.onopen = function() {
            console.log('insdie conn.onopen()');
        
            // send first msg to websocket
            sendmsg(index=null, stage='start', msg=null, example='webapp');


        };

        // sockjs onMessage event triggered whenever there is a message sent on the connection
        conn.onmessage = function(e) {
            console.log('insdie conn.onmessage()');
        
            var m = JSON.parse(e.data);

            console.log('Message received : ',m);

            var msg_type = m.msg_type; 

            if (msg_type === 'suggestion') 
            {
                console.log('insdie msg_type === suggestion');
        
                handleSuggestion(m.msg);
            } 
            else if (msg_type === 'in-app')
            {
                console.log('insdie msg_type === in-app');
        
                handleInApp(m.msg);
            }
            else if (msg_type === 'data')
            {
                console.log('insdie msg_type === data');
        
                handleData(m.msg);
            }
        };

        // sockjs on Close event triggered whenever there is a close event either triggered by
        // server or by user itself via disconnect button -> disconnect()
        conn.onclose = function() {
            console.log('insdie conn.onclose()');
        
            $('.suggestion_row')

            if (errorconn !== 1) 
            {
                console.log('insdie errorconn !== 1');
        
                if (disconn === 0) 
                {
                    console.log('insdie disconn === 0');

                    serverUnavailable();
                } 
                else 
                {
                    console.log('insdie disconn !== 0');

                    disconn = 0;

                    if (connAgain === 1)
                    {
                        connect();
                    }
                }
            } 
            else if (errorconn === 1) 
            {
                console.log('insdie errorconn === 1');

                serverError();
                errorconn = 0;
            }
            
        
        };

        // sockjs Error event triggered whenver there is an error connecting to the connection or
        // error info sent by server
        conn.onerror = function() {
            console.log('insdie conn.onerror');

            errorconn = 1;
        };

        console.log('returning from connect()');
        
    }



    

    
    // function to handle search results of type in-app
    function handleInApp(msg) {
        console.log('inside handleInApp()');

        // deelte old suggestion list
        $sbox.empty();

        // create new suggestion list from new msg received
        var i = 1; 

        var title = '';
        var subtitle = '';
        var category = '';
        var condition = '';

        for (var score in msg)
        {
            if (msg.hasOwnProperty(score))
            {   
                console.log('object : ', msg[score]);

                title = msg[score]['title'];
                subtitle = msg[score]['subtitle'];
                category = msg[score]['category'];
                condition = '';

                if ( i == 1 )
                {
                    i = 2;
                    condition = 'list-group-item-first';
                    
                }
                
                $sbox.append('<a href="#" class="list-group-item ' + condition + ' sugg_title" >').html(title).append('<span class="sugg_cat" >').html(category).append('<br><span class="sugg_subtitle" >').html(subtitle);
                
            }
        }

        console.log('returning from handleInApp');
    }







    // Events on input box focos in
    $('.search_box input').focusin(function(){
        console.log('inside input.focusi()');

        console.log('diabled : '+disabled+' dis : '+dis);

        $('.search_form').addClass('search_focus'); 

        if ((disabled === true) && (dis === 0))
        {
            alert('Please select a suggestion type first, Suggestions or In-App Data');
            dis = 1;
            disabled = false;

        }
        else if ((disabled === false) && (dis === 1))
        {
            dis = 1;
            $(this).blur();
        }
        else
        {
            dis = 0;

            console.log('inside disabled === false and dis === 0');

            var val = $('.search_box input').val();

            console.log('input value : ', val);

            console.log('val.lenghth : ', val.length);

            if (val.length !== 0)
            {
                console.log('inside val.lenthg !== 0');

                $('.suggestion_row').show();
            }
        }

        console.log('RETURNING TIME -> diabled : '+disabled+' dis : '+dis);

    });


    // Events on input box focos out
    $('.search_box input').focusout(function(){
        console.log('inside input.focusout()');

        console.log('diabled : '+disabled+' dis : '+dis);

        if (dis === 1)
        {
            disabled = true;
            dis = 0;
        }

        $('.search_form').removeClass('search_focus');
        $('.suggestion_row').hide();

        console.log('RETURNING TIME -> diabled : '+disabled+' dis : '+dis);

    });




    // triggers whenever user is Typing...
    $('.search_box input').on("input", function(e) {
        console.log('insdie input.keydown(function(){})');

        console.log('diabled : '+disabled+' dis : '+dis);
        
        console.log('e.keycode : '+e.keycode+' | e.which : '+e.which);

        var code = (e.keyCode ? e.keyCode : e.which);
        
        console.log(' key code : ', code);

        if (code==13) {
            console.log('inside keycode is 13, enter key');

            e.preventDefault();
        }
        else
        {
            console.log('inside keycode not 13, non enter key');

            var val = $('.search_box input').val();

            console.log('input value : ', val);

            console.log('val.lenghth : ', val.length);

            if (val.length !== 0)
            {
                console.log('inside val.lenthg !== 0');

                $('.suggestion_row').show();
                
                sendmsg(index=app[app_type], stage='search', msg=val, example=null);
                
            }
            else
            {
                console.log('inside val.lenth === 0');

                // remove previous suggestion list
                $sbox.empty();

                $('.suggestion_row').hide();
            }       

            console.log('RETURNING TIME -> diabled : '+disabled+' dis : '+dis);
        }
        
    });




    // triggered when text is sent by hitting Enter
    $('.search_box input').submit(function() {
        console.log('insdie .search_box input.submit()');

        console.log('diabled : '+disabled+' dis : '+dis);

        if (disabled === true)
        {
            alert('Please select a suggestion type first, Suggestions or In-App Data');
            // dis = 1;
            // disabled = false;

        }
        else
        {
            // dis = 0;
            formsubmit();
        }

        console.log('RETURNING TIME -> diabled : '+disabled+' dis : '+dis);
        
        return false;
    });



    // triggered when msg is sent by search button
    $('.search_button').click(function() {
        console.log('insdie search_button.click()');

        console.log('diabled : '+disabled+' dis : '+dis);

        if (disabled === true)
        {
            alert('Please select a suggestion type first, Suggestions or In-App Data');
            // dis = 1;
            // disabled = false;

        }
        else
        {
            // dis = 0;
            formsubmit();
        }

        console.log('RETURNING TIME -> diabled : '+disabled+' dis : '+dis);

        return false;
    });



    //  sends the message content to sendmsg -> which actually sends msg to the connection
    function formsubmit() {
        console.log('insdie formsubmit()');

        console.log('diabled : '+disabled+' dis : '+dis);

        var v = $('.search_box input').val();

        sendmsg(index=app[app_type], stage='search', msg=v, example=null);

        console.log('RETURNING TIME -> diabled : '+disabled+' dis : '+dis);

        return false;
    }





    // sends the actual msg after JSONifying it to the connection via conn.send()
    function sendmsg(index, stage, msg, example) {
        console.log('insdie sendmsg()');

        var newmsg = {
            'stage': stage;
        };
        
        if (index !== null)
        {
            newmsg['index'] = index;
        }
        if (msg !== null)
        {
            newmsg['msg'] = msg;
        }
        if (example !== null)
        {
            newmsg['example'] = example;
        }

        
        var res = JSON.stringify(newmsg);

        console.log('senign msg to websesocke conn.send : ', res);
        
        conn.send(res);

        console.log('returning from sendmsg()');
   
    }



     

});