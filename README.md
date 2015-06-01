# phone.kzar.co.uk

## Intro

My simple Twilio end point, mostly something I'm playing with for fun. I plan to add the following functionality:

 - [X] Incoming SMS messages to be forwarded to my email address
 - [X] Incoming SMS that start with secret password to cause an outgoing SMS to be sent
 - [X] Incoming calls to record and send voice mail message to my email address
 - [ ] Incoming calls to be added to conference if hash key is pushed

(So far this is a work in progress)


## Dependencies

- uwsgi
- nginx
- python

### Python modules

- flask
- yaml
- twilio-python


## Usage

To run locally:

    python src/phone.py

Then browse to http://localhost:5000

To deploy:

    bin/deploy
    # (Make sure to create these symlinks the first time):
    # - /etc/nginx/sites-enabled/phone.kzar.co.uk -> /etc/nginx/sites-available/phone.kzar.co.uk
    # - /etc/uwsgi/apps-enabled/phone.kzar.co.uk.ini -> /home/apps/phone.kzar.co.uk/config/phone.kzar.co.uk.ini

Then http://phone.kzar.co.uk/ should respond to requests.


## License

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
