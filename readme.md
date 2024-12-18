## Kovaak Aim Trainer Data Acquisition App
### Main Idea
Acquire positional data from the target and user aim from an aim training task and store it after the session is completed with the score.
### Requirements
- Make positional data from both aim position on the screen and target position available for downstream use cases as ML and Analytics.
- Ingest the data during the task, process it after the task and store the processed data for downstream uses. (Ideal/Automated).
- Ingest data from the recorded task video and user aim positions. (Simpler/Manual)
- Final data will be made available in batches.
### Considerations
- The source system should be developed, since Kovaak does not provide the position of the target, nor the cursor position.
- It will be needed to synchronize in time the users aim position and the target position records.
- It will be needed to rescale both positions to the same scale in order to make the positional data comparable.
- Time synchronization can be achieved by running the acquisition source system for user aim and target in parallel, or by synchronizing data from both using the timestamp afterwards.
- For object video recognition a AI API should be used
- The source system should be able to recognized different types and colors of target
- Validate data considering the area of the recognized object
- Modular and Reversible components
- Source System ←→ Ingestion ←→ Validation/Transformation ←→ Serving (.csv)
- One script for each module
- Modules communicate via files 
- Invest on CI/CD
- Scan both user aim and target from the video
- User aim can be just the center of the screen, since the video will be always aligned


