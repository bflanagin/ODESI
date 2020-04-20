# Chat Module
Please refer to the the modules page for any definitions used in this document that may not be clear.

OpenSeed-chat is a lowest common denominator encrypted chat service for individuals and groups using the OpenSeed hierarchical security setup.

## Current implementation:
The chat module was designed with applications and games in mind where in these systems would control the flow of the chat based on the needs of the application and using the applications built in timing. Thus a application dependent on chat may query the server every second where an app that is less dependent may decrease the update requests for bandwidth or other issues.

P2P chat: The standard chat model within OpenSeed. Users have consented to the connection an have shared (via OpenSeed) the encryption key. No users can be added to this chat and will continue to be valid as long as the users of the chat retain the key.

Group chat: Group chats come in two modes, an open mode where any user can join the chat as long as they are authenticated, and private groups whose list is controlled by the creator of the group.

Using OpenSeed-chat:
This module requires an active developer, application, and valid user account on OpenSeed to complete the transaction.

A chat session works in this order.

User initiates a chat with another user via request. If the request has be accepted the two are now able to chat.

The User is now "linked" with the other User and can starts chats with them at any time. If a chat room has not been created for them a new room is created with a new encryption key.

The users can now chat using this key.

If one of the users removes their consent from the chat the link is broken and chatting between the users isn't allowed until the link is re-established.

NOTE: We will assume you have your accounts in order for the next section.

Almost all (soon to be all) functions in OpenSeed will return a json formatted response to a json formatted request.

Example:

{"act":"get_chat","appID":"'+str(OpenSeed.appId)+'","devID":"'+str(OpenSeed.devId)+'","uid":"'+uid+'","username2":"'+username2+'","room":"'+username+','+username2+'","last":"'+str(last)+'"}

Will return:

{"index":number,"message":encrypted data,"date":date,"type":type}

The above is from the Godot library but the Qt version is very similar. The webapp version will need to be changed slightly due to security concerns.

For ease-of-use the OpenSeed library shortens these calls to a simpler uniform function that spans the library regardless to the toolkit.

The functions are a follows with a brief explanation of their task (if it isn't obvious)

check_chat(uid,username2) : Checks for the existence and status of a chat room. These range from 0 - 3 with 0 meaning there is no chat room to 3 meaning the room is closed.

start_chat(uid, username2) : Initializes a chat between two users, using the uid of the first user to verify that the chat is indeed created by the owner of the account. This function creates the encryption key on the server for the users to share.

register_chat(uid,username2) : If the chatroom is created you must register to receive the key.

Note: The above commands would best work in conjunction with each other where in you would check, then either register or start the chat depending on the response. It is kept separate for the rare cases when they might be useful as single functions.

send_chat(uid,username1, username2, message) : Sends chat message to the appointed chatroom. The message is encrypted before sending the message and stored as a binary blob.

get_chat(uid,username2) : Gets chat for the selected users.

 Add a custom footer

