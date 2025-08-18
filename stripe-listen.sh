#!/usr/bin/env bash

stripe listen --forward-to localhost:5080/v1/stripe/callback

