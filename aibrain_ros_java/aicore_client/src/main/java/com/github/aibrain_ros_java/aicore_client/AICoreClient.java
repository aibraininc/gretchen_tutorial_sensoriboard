/*
 * Copyright (C) 2014 jacob.
 * 
 * Licensed under the Apache License, Version 2.0 (the "License"); you may not
 * use this file except in compliance with the License. You may obtain a copy of
 * the License at
 * 
 * http://www.apache.org/licenses/LICENSE-2.0
 * 
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
 * WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
 * License for the specific language governing permissions and limitations under
 * the License.
 */

package com.github.rosjava.aibrain_ros_java.aicore_client;

import org.apache.commons.logging.Log;
import org.ros.message.MessageListener;
import org.ros.namespace.GraphName;
import org.ros.node.AbstractNodeMain;
import org.ros.node.ConnectedNode;
import org.ros.node.NodeMain;
import org.ros.node.topic.Subscriber;
import org.ros.node.topic.Publisher;
import com.aibrain.aicoreclient.AICoReForGretchen;
import java.io.IOException;
/**
   * A simple {@link Subscriber} {@link NodeMain}.
 */
public class AICoreClient extends AbstractNodeMain implements MessageListener<std_msgs.String>{

  Subscriber<std_msgs.String> mSpeechSub;
  Subscriber<std_msgs.String> mUserNameSub;
  Publisher<std_msgs.String> mAICoreAnswerPub;
  Log mLog;
  AICoReForGretchen ag;
  String userName = "Wally";

  @Override
  public GraphName getDefaultNodeName() {
    return GraphName.of("aicore/client");
  }

  @Override
  public void onStart(ConnectedNode connectedNode) {

    // Init ros subscriber and publisher
    mLog = connectedNode.getLog();

    mUserNameSub = connectedNode.newSubscriber("/aicore/username", std_msgs.String._TYPE);
    mSpeechSub = connectedNode.newSubscriber("aicore/input", std_msgs.String._TYPE);
    mAICoreAnswerPub = connectedNode.newPublisher("/aicore/output", std_msgs.String._TYPE);
    mSpeechSub.addMessageListener(this);
    mUserNameSub.addMessageListener(new MessageListener<std_msgs.String>() {
        @Override
        public void onNewMessage(std_msgs.String message) {
          System.out.println("I heard: \"" + message.getData() + "\"");
          userName = message.getData();
        }
    });

    // Init AIcore client
    try {
      String aICORE_HOST= "3.16.127.106";
      ag = new AICoReForGretchen(aICORE_HOST);
      String result = ag.sendMessage(userName, "Hello", "normal");
      System.out.println(result);
      System.out.println("AICoRe Connection success");
    } catch (Exception e) {
      e.printStackTrace();
      mLog.info("AICoRe Connection fail");
      ag =  null;
    }
  }

  @Override
  public void onNewMessage(std_msgs.String message) {
    // When client receives speech message, this function is called.
    System.out.println("I heard: \"" + message.getData() + "\"");
    if(message.getData().length() >3){
      if(ag != null)
        sendTextToAICore(message.getData());
    }
  }

  void sendTextToAICore(String text){
    // Send text to AICore Server
    System.out.println("account name is \"" + userName + "\"");
    try {
      String result = ag.sendMessage(userName, text, "normal");
      System.out.println(result);

      String[] message = result.split("\\$");
      System.out.println("onReceiveMessageFromAICore");
      System.out.println(message[0]);
      System.out.println("length "+message.length);
      if(message.length >1)
      {
        std_msgs.String str = mAICoreAnswerPub.newMessage();
        str.setData(message[1]);
        System.out.println(str);
        mAICoreAnswerPub.publish(str);
      }   

    } catch (Exception e) {
      e.printStackTrace();
    }
  }

}
