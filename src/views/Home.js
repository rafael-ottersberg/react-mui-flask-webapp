import React from 'react';
import Tile from '../components/Tile';
import { Box, CardContent, Grid, Typography } from '@mui/material';

const Home = () => {
  return (
    <Grid container spacing={2}>
      <Grid item xs={6} md={4} sx={{ display: { xs: 'flex', md: 'none' } }}>
        <Tile>
          <SmallLogoContent />
        </Tile>
      </Grid>

      <Grid
        item
        xs={6}
        md={8}
        sx={{ display: { xs: 'none', sm: 'none', md: 'flex' } }}
      >
        <Tile>
          <LargeLogoContent />
        </Tile>
      </Grid>
    </Grid>
  );
};

export default Home;

const SmallLogoContent = () => {
  return (
    <React.Fragment>
      <CardContent
        sx={{
          height: '100%',
        }}
      >
        <Box
          sx={{
            justifyContent: 'center',
            alignItems: 'center',
            display: { xs: 'flex', sm: 'none' },
            flexDirection: 'column',
            height: '100%',
          }}
        >
          <Typography sx={{ mt: 3, textAlign: 'center' }} variant="h7">
            26.-29. Mai 2022
          </Typography>
        </Box>
        <Box
          sx={{
            justifyContent: 'center',
            alignItems: 'center',
            display: { xs: 'none', sm: 'flex' },
            flexDirection: 'column',
            height: '100%',
          }}
        >
          <Typography sx={{ mt: 3, textAlign: 'center' }} variant="h4">
            26. bis 29. Mai 2022
          </Typography>
        </Box>
      </CardContent>
    </React.Fragment>
  );
};

const LargeLogoContent = () => {
  return (
    <CardContent>
      <Box
        sx={{
          justifyContent: 'center',
          alignItems: 'center',
          display: 'flex',
          flexDirection: 'column',
        }}
      >
        <Typography sx={{ mt: 3, textAlign: 'center' }} variant="h4">
          26. bis 29. Mai 2022
        </Typography>
      </Box>
    </CardContent>
  );
};