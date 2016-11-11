# CITS5503 Voice Verification

James Hercock, 21308586

## Requirements:

This project fulfills the functional requirement of being able to register a user with a user provided name and to create a profile and voice enrolment associated with that name. It also fulfills the requirement of being able to verify a user that provides their name by using their voice. Due to the fact that the internet is being used for this service, there is inherently some latency and therefore this implementation fails to fulfill the non-functional requirement of being able to serve users quickly in a voting scenario.

## To run this project:

1. Edit the verifKey variable near the top of project.py to contain the API key for your Speech Verification subscription.
2. Open a command prompt (preferably with admin privileges).
3. Navigate to the folder the project is downloaded to.
4. If this is the first time running the project, run &quot;pip install -r requirements.txt&quot; in the command prompt.
5. Run &quot;python Project.py&quot;
6. A GUI should appear, this is the project.

## How to use:

On the entry screen there are 3 options, &quot;Enrol New User&quot;, &quot;Verify User For Vote&quot;, and &quot;See Votes&quot;.

### All are fairly self explanatory;

- &quot;Enrol New User&quot; creates a new user profile and attempts to enrol their voice.
- &quot;Verify Enrolled User&quot; takes a name and checks it against the database, then allows the user to attempt to verify their voice before then allowing them to vote if they successfully verify.
- &quot;See Votes&quot; allows a user to view the stored votes, with a single comment in the code can be disabled if such functionality is not desired.

## NOTES:

- For enrolment, duplicate names are not allowed. The project will verbally warn the user that the name entered already exists if attempted.
- The project requires internet connectivity to function.
- Since the speech client uses the internet to talk to the user, the speed of the internet connection will affect how responsive the project is.
- While the program is talking to the user, no other actions can be taken. This includes the recording of the user&#39;s voice, so the user must wait for the program to finish before responding with their passphrase.
- Currently the implementation uses a locally stored file to store both votes and profile IDs, this functions when running on only one machine, but full deployment will require storing votes and profile IDs to a cloud provider&#39;s storage service.
- Similarly to the last point, the API key for making use of the voice verification and text-to-speech are hard-coded into the project. In a real deployment such keys would not be handled directly but rather use a service like Azure's keyvault or similar.

## References:

Recording code from: [https://github.com/ayush1794/wave\_mixer/blob/master/recording.py](https://github.com/ayush1794/wave_mixer/blob/master/recording.py)

Code handling API requests from: [https://github.com/Microsoft/Cognitive-SpeakerRecognition-Python/tree/master/Verification](https://github.com/Microsoft/Cognitive-SpeakerRecognition-Python/tree/master/Verification)
(With some modifications to add return statements)
