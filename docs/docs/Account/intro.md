Current existing functions found in the OpenSeed_Account file. Not all these functions are finalized and there will be changes while we work toward our first release. However, these should represent most of the major features.

**check_appID(appID,devID)**: Used to check the applications status on OpenSeed. If it returns true the application is free to use the service.

**check_devID(name)**: Used to access the developer account. Misnomer this checks if the user is also a developer.

**account_check(username,passphrase)**: Checks user accounts returns true if correct.

**create_user(username,passphrase,email)**: Creates Account based on the included criteria

**create_creator_account(devName,contactName,contactEmail,openseed)**: Creates Developer account

**create_app(devID,appName)**: Creates Application and associates it with the developer.

**create_profile(theid,data1,data2,data3,data4,data5,thetype)**: Creates the long form profile for users,developers, and applications. Called after the ids have been created.

**update_history(userid,apppubId,data)** : Adds to the history record for the user

**get_history(userid,apppubId,count)** : Returns the history for a specific account. Optionally you may define a specific application and a total count.
