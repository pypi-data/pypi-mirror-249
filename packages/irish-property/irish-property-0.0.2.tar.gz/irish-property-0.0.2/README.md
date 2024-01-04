# Irish Property Buy/Rent Notification Tool

<img src="/assets/screenshot.jpg" alt="screenshot" style="height: 464px; width:214px;"/>

Tool to help in finding the right home and to avoid having to interact with the web tools which aren't great to use.

Currently aggregates from Daft.ie, MyHome.ie, and Property&#46;ie

Uses ntfy to get mobile notifications of new properties listed.


## Install

`python -m pip install irish_property`


## Usage

Modify your preferences in settings and input a custom name for a ntfy channel if you are planning on using ntfy (no sign up required, very easy to set up). It can be a bit annoying to configure for each of the websites, going to work on this to try have one setting for all three. Should probably make a tool to generate the config.

To set up configuration run `irish_property_finder_add_config`. You will be asked questions about how things should be filtered.

To print out all listings per config run `irish_property_find`

To run the notification service on a loop run `irish_property_run_ntfy`. To run once without looping run `irish_property_run_ntfy --once`

To clear the persistence run `irish_property_remove_persistence` or remove the file in `settings.SHELVE_LOCATION`

To remove configs, remove the file in `/opt/irish_property/configs`
