#!/bin/bash

#jupyter nbconvert --to script [YOUR_NOTEBOOK].ipynb

#client_note_recipient.ipynb
#CS_client_note.ipynb # OK
#CS_client_note_last_touch.ipynb #OK
#CS_client_note_recipient.ipynb # OK
#CS_client_note_times.ipynb #OK
#CS_client_note_trajectories.ipynb # OK
#mv CS_client_subscription.ipynb client_subscription.ipynb #OK
#mv CS_disposition.ipynb disposition.ipynb #OK
#mv CS_feature.ipynb feature.ipynb #OK
#mv CS_model.ipynb model.ipynb #OK
#mv CS_tenant_client.ipynb tenant_client.ipynb #OK
#mv CS_tenant.ipynb tenant.ipynb #OK
#CS_outcome.ipynb
#CS_plots.ipynb
#CS_tables.ipynb



# jupyter nbconvert --to script client_note_recipient.ipynb 
# jupyter nbconvert --to script client_note_trajectories.ipynb 
# jupyter nbconvert --to script disposition.ipynb 
# jupyter nbconvert --to script tenant_client.ipynb 
# jupyter nbconvert --to script tenant.ipynb 
# jupyter nbconvert --to script client_note_recipient.ipynb



jupyter nbconvert --to script client_subscription.ipynb 
jupyter nbconvert --to script client_note.ipynb
# jupyter nbconvert --to script client_note_times.ipynb 
# jupyter nbconvert --to script client_note_last_touch.ipynb 
# jupyter nbconvert --to script feature.ipynb 
jupyter nbconvert --to script combineFeatures.ipynb
jupyter nbconvert --to script model.ipynb 
