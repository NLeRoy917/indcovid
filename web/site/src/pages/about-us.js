import React from "react"
import styled from 'styled-components';

import Layout from "../components/layout";
import SEO from "../components/seo";
import InfoSection from '../components/moreinfosection';
import Nav from '../components/nav';

import barnabas from '../images/barnabas.png';
import nathan from '../images/nathan.png';
import mph_logo from '../images/mph-logo.svg';
import ind_gov from '../images/ind-gov.png';
import cdc_logo from '../images/cdc.png'

import {
  useMediaQuery,
  Grid
} from '@material-ui/core';

const InlineLink = styled.a`
    color: rgba(75,192,192,0.9);
`

const MediaWrapper = styled.div`
    display: flex !important;
    justify-content: center !important;
    align-items: center !important;
`

const ImgLink = styled.a`
  text-decoration: none;
  &:hover {
    text-decoration: none;
  }
  &:active {
    text-decoration: none;
  }
  &:focus {
    text-decoration: none;
  }
`

const Img = styled.img`
    overflow: hidden;
    border-radius: 50%;
    transition: ease 0.1s;
    width: 150px;
    height: 150px;
    margin: 10px;
    border: white 1px solid;
    &:hover {
      cursor: pointer;
      box-shadow: 5px 5px white, 4px 4px white, 3px 3px white, 2px 2px white, 1px 1px white;
      transform: translate(-5px, -5px);
    }
    &:active {
        transform: translate(-4px,-4px);
        box-shadow: 4px 4px white, 3px 3px white, 2px 2px white, 1px 1px white;
    }
`

const LogoImg = styled.img`
  height: 75px;
  width: auto;
  margin: 10px;
`

const AboutUsPage = () => {

    const mobile = useMediaQuery('(max-width:480px)', { noSsr: true });

    return (
    <Layout>
      <SEO 
        title="About Us" 
        description="In this research, we take the time to analyze and invstigate how people from under-privileged communities are disproportionately affected by the COVID-19 pandemic."
        lang="en"
        meta="Indiana COVID-19 & Health Equity"
        />
      {mobile ? '' : <Nav />}
      <InfoSection
        title="Developers"
        content="This site was developed by Barnabas Obeng-Gyasi and Nathan LeRoy. Both graduates of Purdue University, Nathan now works for the Indiana Biosciences Research Institute as an Assistant Research Associate. Barnabas currently works as a Senior Research Assistant at Duke University and is preparing for medical school."
        media={
            <>
              <MediaWrapper>
                <ImgLink href="https://www.linkedin.com/in/barnabas-obeng-gyasi-8baba3191/">
                   <Img src={barnabas} style={{backgroundSize: '200%'}}/>
                </ImgLink>
                <ImgLink href="https://www.linkedin.com/in/nathanjleroy/">
                   <Img src={nathan} />
                </ImgLink>
              </MediaWrapper>
            </>
        }
      />
      <br></br>
      <InfoSection
        title="Data Sources"
        content={
        <><div>Our data is pulled from <InlineLink href="https://hub.mph.in.gov/dataset?q=COVID">Indiana Data Hub's</InlineLink> daily updated statistics on coronavirus. This is then run through the program ArcGIS to create map data. Analysis takes this data and frames it within a <InlineLink href="https://svi.cdc.gov/">Social Vulnerability Index (SVI)</InlineLink> which gives us a set of societal domains to display the statistics. This allows us to identify the potential for different race-based and socioeconomic disparities in communities in indiana.</div>
        <br></br>
        <div>
        In addition, we turn to <InlineLink href="https://www.cdc.gov/coronavirus/2019-ncov/">the CDC</InlineLink> for all guidance on public health and safety recommendations and procedures.
        </div>
        <div style={{padding: '5px', fontSize: '0.9rem'}}>
        <em>Note: No direct conclusions were drawn from the data simply the identification for areas of inequity and the visualization of the pandemic.</em>
        </div></>
        }
        media={
            <>
              <MediaWrapper>
                <Grid container
                 direction="column"
                 alignItems="center"
                 justify="center"
                 >
                   <Grid item>
                    <LogoImg src={mph_logo} />
                   </Grid>
                   <Grid item>
                    <LogoImg src={cdc_logo} />
                   </Grid>
                   <Grid item>
                    <LogoImg src={ind_gov} />
                  </Grid>
                 </Grid>
              </MediaWrapper>
            </>
        }
      />
    </Layout>
  )
}
  
  export default AboutUsPage;
  