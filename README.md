# ShadowHero

ShadowHero is an automated online harassment countermeasure agent designed to identify
harassment situations when they happen and take appropriate action.

# The MLH + Hack Harassment Challenge

http://www.hackharassment.com/mlh/

ShadowHero has been created for the Hack Harassment Challenge with the goal of
identifying and reducing online harassment.

# Running the project

1. Clone this repository: 'git clone https://github.com/gunthercox/ShadowHero/'
2. Change directory: `cd ShadowHero`
3. `git clone https://github.com/HackHarassment/TwitterClassifier.git`
4. Extract the zipped files in the TwitterClassifier data directory
5. Create a file called `settings.py` with the following data:

```python
GITTER = {
    'API_TOKEN': 'my-gitter-agent-api-token',
    'ROOM': 'gitter_account_name/gitter_room_name'
}
```