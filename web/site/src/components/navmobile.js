import React from 'react';
import styled from 'styled-components';

import {
    Drawer,
    List,
    ListItem
} from '@material-ui/core';
import LocalHospitalIcon from '@material-ui/icons/LocalHospital';
import PeopleIcon from '@material-ui/icons/People';
import EventAvailableIcon from '@material-ui/icons/EventAvailable';
import CodeIcon from '@material-ui/icons/Code';
import ColorizeIcon from '@material-ui/icons/Colorize';
import IndianaIcon from '../images/Info-Thick.svg';

const DrawerContainer = styled(Drawer)`

`

const InnerWrapper = styled.div`
    color: white;
    background-color: #2f2f2f !important;
    height: 100%;
    width: 100%
`

const ALink = styled.a`
  color: inherit;
  font-size: 1rem;
  text-decoration: none;
  height: 100%;
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

const NavMobile = ({ open, setOpen}) => {
    return(
        <>
        <DrawerContainer
          variant="temporary"
          anchor="left"
          open={open}
          onClick={setOpen}
        >
        <InnerWrapper>
        <List>
          <ListItem>
            <PeopleIcon fill='white'  style={{margin: '5px'}}/>
              <ALink href="/">
                Health Equity
              </ALink>
          </ListItem>
          <ListItem>
              <LocalHospitalIcon fill='white' style={{margin: '5px'}}/>
              <ALink href="/stay-healthy">
                Stay Healthy
              </ALink>
          </ListItem>
          <ListItem>
              <EventAvailableIcon fill="white" style={{margin: '5px'}} />
              <ALink href="/back-on-track">
                  Back On Track
              </ALink>
          </ListItem>
          <ListItem>
            <img
              alt="Indiana outline"
              src={IndianaIcon}
              style={{fill: '#e3e3e3', height: '20px', width: 'auto', marginLeft: '11px', marginRight: '11px', marginTop: '5px', marginBottom: '5px'}}
            />
            <ALink href="/more-info">
              More Info
            </ALink>
          </ListItem>
          <ListItem>
            <CodeIcon fill='white'  style={{margin: '5px'}}/>
            <ALink href="/about-us">
              About Us
            </ALink>
          </ListItem>
          <ListItem>
            <ColorizeIcon fill='white'  style={{margin: '5px'}}/>
            <ALink href="/vaccine">
              Vaccine
            </ALink>
          </ListItem>
        </List> 
        </InnerWrapper>   
        </DrawerContainer>
        </>
    )
}

export default NavMobile;