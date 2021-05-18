import React from 'react';
import chordmaster from '../../static/images/chordmaster.jpg';

function Logo() {
  console.log(chordmaster)
  return (
    <div className="Logo">
      <img src={chordmaster} alt="Chord Master" height={50} width={200} />
    </div>
  );
}

export default Logo
