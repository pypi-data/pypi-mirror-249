# Helloasso to Discourse

This works in two distinct steps: first fetch HelloAsso data, then sync with Discourse.


## Installing

    pip install .


## Using

### 1 — Fetch HelloAsso data

Use the `fetch` subcommand, I use it as is:

    $ helloasso-to-discourse fetch "$(pass helloasso-clientid)" "$(pass helloasso-clientsecret)" afpy

this fetches the data of the given organization, here named `afpy`, it creates an `./afpy` file.


### 2 — Choose what to sync

The goal is to sync an HelloAsso event (they call it `forms`) to a Discourse Badge.

First let's discover which HelloAsso 'forms' we can use:

    $ helloasso-to-discourse list-forms ./afpy

Then let's discover which Discourse badges we can use:

    $ helloasso-to-discourse list-badges https://discuss.afpy.org "$(pass discuss.afpy.org-api-key)"


### 3 — Sync

This step actually assigns badges to Discourse users:

As an example to assign badge "membre" to HelloAsso users having paid for the form named `adhesion-2023-a-l-afpy`:

    $ helloasso-to-discourse sync https://discuss.afpy.org "$(pass discuss.afpy.org-api-key)" ./afpy adhesion-2023-a-l-afpy membre

And an exemple to assign Discourse badge `pyconfr-2023` to members having registered for the `pyconfr-2023` event on HelloAsso:

    $ helloasso-to-discourse sync https://discuss.afpy.org "$(pass discuss.afpy.org-api-key)" ./afpy pyconfr-2023 pyconfr-2023
