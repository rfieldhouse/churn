#!/bin/bash
sed -i "s/get_ipython().magic(u'matplotlib inline')//g" client_subscription.py
sed -i "s/get_ipython().magic(u'matplotlib inline')//g" client_note.py
#sed -i "s/get_ipython().magic(u'matplotlib inline')//g" client_note_times.py
#sed -i "s/get_ipython().magic(u'matplotlib inline')//g" client_note_last_touch.py
#sed -i "s/get_ipython().magic(u'matplotlib inline')//g" feature.py
sed -i "s/get_ipython().magic(u'matplotlib inline')//g" combineFeatures.py
sed -i "s/get_ipython().magic(u'matplotlib inline')//g" model.py

sed -i "s/'# In[ ]:'//g" client_note.py