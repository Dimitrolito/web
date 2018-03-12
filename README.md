<img src='https://d3vv6lp55qjaqc.cloudfront.net/items/263e3q1M2Y2r3L1X3c2y/helmet.png'/>

# Gitcoin

Gitcoin pushes Open Source Forward. Learn more at [https://gitcoin.co](https://gitcoin.co)

# web repo

[![Build Status](https://travis-ci.org/gitcoinco/web.svg?branch=master)](https://travis-ci.org/gitcoinco/web)
[![codecov](https://codecov.io/gh/gitcoinco/web/branch/master/graph/badge.svg)](https://codecov.io/gh/gitcoinco/web)
[![Waffle.io - Columns and their card count](https://badge.waffle.io/gitcoinco/web.svg?columns=all)](https://waffle.io/gitcoinco/web)

This is the website that is live at gitcoin.co

## How to interact with this repo

### On Github

[Star](https://github.com/gitcoinco/web/stargazers) and [watch](https://github.com/gitcoinco/web/watchers) this github repository to stay up to date, we're pushing new code several times per week!

Check out the [CHANGELOG](./CHANGELOG.md) for details about recent changes to this repository.

Also,

* want to become a contributor ? Checkout our [guidelines](./docs/CONTRIBUTING.md).
* [check out the gitcoinco organization-wide repo](https://github.com/gitcoinco/gitcoinco).
* check out the open issues list, especially the [discussion](https://github.com/gitcoinco/web/issues?q=is%3Aissue+is%3Aopen+label%3Adiscussion) label and [easy-pickings](https://github.com/gitcoinco/web/issues?q=is%3Aissue+is%3Aopen+label%3Aeasy-pickings).

### On Gitcoin

<a href="https://gitcoin.co/explorer/?q=https://github.com/gitcoinco/web">
    Check out the available open issues on Gitcoin.
</a>

## What

Functionally, the app has several key features:

* Smart Contracts -- Where funded issues are stored and indexed.
* Brochureware -- Describes the project.
* Funded Issue Explorer -- A searchable index of all of the work available in the system.
* Funded Issue Submission / Acceptance flow -- Interface between the application and web3.
* API - the HTTPS API
* Bot - the GitcoinBot

[More about how/why to interact with web3 here](https://gitcoin.co/web3).

Technically, the system is architected:

* __Web3__ The main source of truth for the system is the Ethereum blockchain. Check out the [smart contracts](https://github.com/gitcoinco/smart_contracts).
* __Web2__ This part of the app is built with Python, Django, Postgres, and a handful of other tools that are common in the web2 ecosystem.
* __Web 3 Bridge__ This is the bridge between web3 and the rest of the application. Mostly built in javascript(web3js) and python(web3py).
* __Brochureware__ Just a nice little landing page telling folks what the Gitcoin project is.

# HTTPS API

[For more information on the HTTPS API, please view the api README](readme_api.md)

# Running Locally

[For more information on running the app locally, please view the running locally README](readme_runninglocally.md)


# Adding your token to Gitcoin.

Have an ERC20 compatible token that you'ud like to add support for?  Great!

[Here is an example of how to do it](https://github.com/gitcoinco/web/pull/155)

# Legal

'''
    Copyright (C) 2017 Gitcoin Core

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as published
    by the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
    GNU Affero General Public License for more details.

    You should have received a copy of the GNU Affero General Public License
    along with this program. If not, see <http://www.gnu.org/licenses/>.

'''

# License
[GNU AFFERO GENERAL PUBLIC LICENSE](./docs/LICENSE)

<!-- Google Analytics -->
<img src='https://ga-beacon.appspot.com/UA-102304388-1/gitcoinco/web' style='width:1px; height:1px;' >
