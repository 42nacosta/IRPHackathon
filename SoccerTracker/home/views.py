from django.shortcuts import render
import matplotlib.pyplot as plt
import numpy as np
import requests
import pandas as pd
import json
from mplsoccer import Pitch ,VerticalPitch
from skillcorner.client import SkillcornerClient
import streamlit as st


# Create your views here.
def index(request):

    return render(request, 'home/index.html')

def about(request):
    return render(request, 'home/about.html')

