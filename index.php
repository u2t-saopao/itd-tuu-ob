<?php 
	/*Get Data From POST Http Request*/
	$datas = file_get_contents('php://input');
	/*Decode Json From LINE Data Body*/
	$deCode = json_decode($datas,true);


	file_put_contents('log.txt', file_get_contents('php://input') . PHP_EOL, FILE_APPEND);

	$replyToken = $deCode['events'][0]['replyToken'];
	$recv_msg = $deCode['events'][0]['message']['text'];



	$messages = [];
	$messages['replyToken'] = $replyToken;
	$rep_msg = [];
    //$url = "https://api.thingspeak.com/channels/1632897/feeds.json?results=1";
    
    if($recv_msg == "Hi") {
		$rep_msg ['text'] = "Hi";
		$rep_msg ['type'] = 'text';
    else if($recv_msg == "l1") {
        $url = "https://api.thingspeak.com/channels/1632897/feeds.json?results=1";
        $strRet = file_get_contents($url);
		//$strRet = json_decode($strRet);
		//$light1 = $strRet->feeds[0]->field1;
		$rep_msg['text'] = $strRet;
		$rep_msg['type']='text';
	}else if($recv_msg == "light1 OFF") {
		$strRet = file_get_contents($url);
		$strRet = json_decode($strRet);
		$light1 = $strRet->feeds[0]->field1;
            if($light1 == "1"){
                $l1 = "https://api.thingspeak.com/update?api_key=ZRZROJRHC73CR4LJ&field1=0";
            }else ($light1 == "0"){
                $l1 = "https://api.thingspeak.com/update?api_key=ZRZROJRHC73CR4LJ&field1=0";
            }
		$rep_msg['text'] = "light1 OFF";
		$rep_msg['type']='text';
	}else if($recv_msg == "light2 ON") {
		$url = "https://api.thingspeak.com/update?api_key=ZRZROJRHC73CR4LJ&field2=1";
		$strRet = file_get_contents($url);
		$strRet = json_decode($strRet);
		$pm = $strRet->feeds[0]->field3;
		$rep_msg['text'] = $pm;
		$rep_msg['type']='text';
	}else if($recv_msg == "light2 OFF") {
		$url = "https://api.thingspeak.com/update?api_key=ZRZROJRHC73CR4LJ&field2=0";
		$strRet = file_get_contents($url);
		$strRet = json_decode($strRet);
		$pict = $strRet->feeds[0]->field4;
		$rep_msg['text'] = $pict;
		$rep_msg['type']='text';
	}else if($recv_msg == "Temp") {
		$rep_msg['originalContentUrl'] = "https://thingspeak.com/channels/1632897/charts/3";
		$rep_msg['previewImageUrl'] = "https://thingspeak.com/channels/1632897/charts/3";
		$rep_msg['type']='image';
    }else if($recv_msg == "Electric") {
		$url = "https://api.thingspeak.com/channels/1555446/feeds.json?results=1";
		$strRet = file_get_contents($url);
		$strRet = json_decode($strRet);
		$dash = $strRet->feeds[0]->field5;
		$rep_msg['text'] = $dash;
		$rep_msg['type']='text';
    }	

	$messages['messages'][0] =  $rep_msg;

	$encodeJson = json_encode($messages);

	$LINEDatas['url'] = "https://api.line.me/v2/bot/message/reply";
 	$LINEDatas['token'] = "2HXDSd8UG3mxBOboLxq15zE3JfUBFqn+2ThJauXxbWVm8ye7zCu5YNxSxOqin2ZDSJVzy65LGKWdGgxUNeppPtIyoLHcTl07xnCDh/kLRhC5b7kadxPEEVrGG48bK5T2XiFTJkzaWiHcZgj9M8KgbAdB04t89/1O/w1cDnyilFU=";
  	$results = sentMessage($encodeJson,$LINEDatas);

	/*Return HTTP Request 200*/
	http_response_code(200);


	function sentMessage($encodeJson,$datas)
	{
		$datasReturn = [];
		$curl = curl_init();
		curl_setopt_array($curl, array(
		  CURLOPT_URL => $datas['url'],
		  CURLOPT_RETURNTRANSFER => true,
		  CURLOPT_ENCODING => "",
		  CURLOPT_MAXREDIRS => 10,
		  CURLOPT_TIMEOUT => 30,
		  CURLOPT_HTTP_VERSION => CURL_HTTP_VERSION_1_1,
		  CURLOPT_CUSTOMREQUEST => "POST",
		  CURLOPT_POSTFIELDS => $encodeJson,
		  CURLOPT_HTTPHEADER => array(
		    "authorization: Bearer ".$datas['token'],
		    "cache-control: no-cache",
		    "content-type: application/json; charset=UTF-8",
		  ),
		));

		$response = curl_exec($curl);
		$err = curl_error($curl);

		curl_close($curl);

		if ($err) {
		    $datasReturn['result'] = 'E';
		    $datasReturn['message'] = $err;
		} else {
		    if($response == "{}"){
			$datasReturn['result'] = 'S';
			$datasReturn['message'] = 'Success';
		    }else{
			$datasReturn['result'] = 'E';
			$datasReturn['message'] = $response;
		    }
		}

		return $datasReturn;
	}
?>