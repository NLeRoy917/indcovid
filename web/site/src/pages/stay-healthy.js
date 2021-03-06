import React from "react"
import styled from 'styled-components';

import Layout from "../components/layout";
import SEO from "../components/seo";
 
import {
  useMediaQuery,
  Typography,
} from '@material-ui/core';

import Nav from '../components/nav';

import wash_hands from '../images/hand-wash.png';
import covid_test from '../images/covid-test.png';
import social_distance from '../images/social-distance.png';
import mask from '../images/mask.png';
import symptoms from '../images/symptoms.png';

const SectionWrapper = styled.div`
  padding: 15px;
  border: solid white 1px;
`
const PageTitle = styled(Typography)`
  font-weight: 400;
  font-size: 1.8rem;
  color: inherit;
  text-align: center;
`

const InlineLink = styled.a`
    color: rgba(75,192,192,0.9);
`

const SectionTitle = styled(Typography)`
    color: inherit;
    font-size: 1.75rem;
    text-align: center;
`

const SectionContent = styled(Typography)`
    color: inherit;
    font-size: 1.75rem;
    font-weight: 300 !important;
`

const Img = styled.img`
    height: 40px;
    width: auto;
    overflow: cover;
    margin-left: 10px;
    margin-right: 10px;
`

const List = styled.ul`
    font-weight: 300;
`

const ListItem = styled.li`

`

const RoundedButton = styled.a`
    text-decoration: none;
    margin: 15px;
    padding: 10px;
    padding-left: 20px;
    padding-right: 20px;
    background: white;
    border: none;
    color: #3b9090;
    border: #3b9090 solid 1px;
    font-family: inherit;
    font-size: 1.00rem;
    transition: ease-in 0.15s;
    border-radius: 30px;
    
    &:hover {
        background: #3b9090;
        color: white;
        border: rgba(0,0,0,0) solid 1px;
        cursor: pointer;
    }
    &:active {
        background: #e6e6e6;
        color: rgba(1,1,1,0.6);
        border: rgba(1,1,1,0.6) solid 2px; 
        transition: 0.4s;
    }
    &:focus {
        outline: none;
    }

`

const StayHealthyPage = () => {

    const mobile = useMediaQuery('(max-width:480px)', { noSsr: true });
    
    return(
    <Layout>
      <SEO 
        title="Stay Healthy" 
        description="In this research, we take the time to analyze and invstigate how people from under-privileged communities are disproportionately affected by the COVID-19 pandemic."
        lang="en"
        meta="Indiana COVID-19 & Health Equity"
      />
      {mobile ? '' : <Nav />}
      <br></br>
      <PageTitle gutterBottom variant="h2">
        Ways to Stay Healthy
      </PageTitle>
      {/* <ButtonWrapper>
        <RoundedButton
          href="https://www.cdc.gov/coronavirus/2019-ncov/index.html"
        >
          CDC Website
        </RoundedButton>
      </ButtonWrapper> */}
        <SectionWrapper
          mobile={mobile}
        >
        <SectionTitle 
              gutterBottom 
              variant="h4"
            >
                Recognize the Symptoms! <Img src={symptoms} />
            </SectionTitle>
            <SectionContent>
                One of the first steps to protecting yourself and others is recognizing the symptoms of COVID-19. If you are experiencing one or more of the symptoms below, contact your healthcare provider right away or get tested.
            </SectionContent>
            <div style={{display: 'flex', alignItems: 'center', justifyContent: 'center'}}>
            <List>
              <ListItem>Fever or chills</ListItem>
              <ListItem>New loss of taste or smell</ListItem>
              <ListItem>Shortness of breath or difficulty breathing</ListItem>
              <ListItem>Congestion or runny nose</ListItem>

              <ListItem>Muscle or body aches</ListItem>
              <ListItem>Weakness</ListItem>
            </List>
            <List>
              <ListItem>Headache</ListItem>
              <ListItem>Cough</ListItem>
              <ListItem>Sore throat</ListItem>
              <ListItem>Fatigue</ListItem>  
              <ListItem>Nausea or vomiting</ListItem>
              <ListItem>Diarrhea</ListItem>
            </List>
          </div>
          <div style={{width: '100%', display: 'flex', justifyContent: 'center'}}>
          <RoundedButton
            href="https://www.cdc.gov/coronavirus/2019-ncov/symptoms-testing/coronavirus-self-checker.html"
          >
            Have Symptoms?
          </RoundedButton>
          </div>
          </SectionWrapper>
      <br></br>
        <SectionWrapper mobile={mobile}>
            <SectionTitle 
              gutterBottom 
              variant="h4"
            >
                Wash Your Hands <Img src={wash_hands} /> 
            </SectionTitle>
            <SectionContent>
                The CDC states that keeping your hands clean is especially important to help prevent the spread of the virus. Wash your hands often with soap and water for at least 20 seconds especially after you have been in a public place, or after blowing your nose, coughing, or sneezing. Its especially important to wash:
            </SectionContent>
            <List>
              <ListItem>Before eating or preparing food</ListItem>
              <ListItem>Before touching your face</ListItem>
              <ListItem>After using the restroom</ListItem>
              <ListItem>After leaving a public place</ListItem>
              <ListItem>After blowing your nose, coughing, or sneezing</ListItem>
              <ListItem>After handling your mask</ListItem>
              <ListItem>After changing a diaper</ListItem>
              <ListItem>After caring for someone sick</ListItem>
              <ListItem>After touching animals or pets</ListItem>
            </List>
        </SectionWrapper>
        <br></br>
        <SectionWrapper mobile={mobile}>
        <SectionTitle 
              gutterBottom 
              variant="h4"
            >
                Get Tested <Img src={covid_test} /> 
            </SectionTitle>
            <SectionContent gutterBottom>
            If you think you have been exposed to COVID-19 and develop a fever and symptoms, such as cough or difficulty breathing, call your healthcare provider for medical advice. If you have a medical appointment, call your doctor’s office or emergency department, and tell them you have or may have COVID-19. This will help the office protect themselves and other patients. You can also consult a healthcare provider through telehealth, if that is an option.
            </SectionContent>
            <div style={{width: '100%', display: 'flex', justifyContent: 'center'}}>
            <RoundedButton 
              variant="outlined" 
              color="inherit"
              href="https://www.hhs.gov/coronavirus/community-based-testing-sites/index.html"
            >
                Get Tested
            </RoundedButton>
          </div>
            </SectionWrapper>
        <br></br>
          <SectionWrapper mobile={mobile}>
            <SectionTitle 
              gutterBottom 
              variant="h4"
            >
                Social Distancing <Img src={social_distance} /> 
            </SectionTitle>
            <SectionContent gutterBottom>
              Social distancing, also called “physical distancing,” means keeping a safe space between yourself and other people who are not from your household. To practice social or physical distancing, stay at least 6 feet (about 2 arms’ length) from other people who are not from your household in both indoor and outdoor spaces.
            </SectionContent>
            <SectionContent gutterBottom>
            {
              <>
                <b>UPDATE (09/02/2020):</b> The Indiana State Department of Health has <InlineLink href="https://www.coronavirus.in.gov/files/20_COVID-19-social%20bubbles%209.2.20.pdf">recommended</InlineLink> that citizens try to refrain from socializing outside a <em>Social Bubble</em>. A Social Bubble is a small group of people who socialize only with each other and gather only when sticking to the same prevention measures. While a social bubble can give you more in-person interactions, it doesn’t mean socializing with everyone you know. Even with steps to stay safe, meeting with others in your social bubble does increase your risk for getting COVID-19, so it’s important that everyone in your small group stays at least 6 feet apart, wears a mask (even when outdoors) and practices good hand hygiene.
              </>
            }
            </SectionContent>
          </SectionWrapper>
          <br></br>
        <SectionWrapper mobile={mobile}>
          <SectionTitle
          gutterBottom
          variant="h4"
          >
            Wear a Mask <Img src={mask}/> 
          </SectionTitle>
          <SectionContent gutterBottom>
          {
            <p>Masks may help prevent people who have COVID-19 from spreading the virus to others. Wearing a mask will help protect people around you, including those at <InlineLink href="https://www.cdc.gov/coronavirus/2019-ncov/need-extra-precautions/people-at-increased-risk.html?CDC_AA_refVal=https%3A%2F%2Fwww.cdc.gov%2Fcoronavirus%2F2019-ncov%2Fneed-extra-precautions%2Fpeople-at-higher-risk.html">higher risk of severe illness</InlineLink> from COVID-19 and workers who frequently come into close contact with other people.Masks are most likely to reduce the spread of COVID-19 when they are widely used by people in public settings. The spread of COVID-19 can be reduced when masks are used along with other <InlineLink href="https://www.cdc.gov/coronavirus/2019-ncov/prevent-getting-sick/prevention.html">preventive measures.</InlineLink>
            </p>
          }
          </SectionContent>
          </SectionWrapper>
    </Layout>
    )
  }
  
  export default StayHealthyPage;
  