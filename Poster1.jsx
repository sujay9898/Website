import React, { useState } from 'react';

const Poster1 = () => {
  const [selectedSize, setSelectedSize] = useState('A3');
  const [selectedFrame, setSelectedFrame] = useState('no');
  const [currentPrice, setCurrentPrice] = useState(159);

  const pricing = {
    'A4': { 'no': 129, 'black': 399, 'white': 399 },
    'A3': { 'no': 159, 'black': 499, 'white': 499 }
  };

  const updatePrice = (size, frame) => {
    setCurrentPrice(pricing[size][frame]);
  };

  const handleSizeChange = (size) => {
    setSelectedSize(size);
    updatePrice(size, selectedFrame);
  };

  const handleFrameChange = (frame) => {
    setSelectedFrame(frame);
    updatePrice(selectedSize, frame);
  };

  const styles = {
    page: {
      backgroundColor: '#1c1c1b',
      minHeight: '100vh',
      padding: '20px',
      fontFamily: 'Inter, sans-serif',
      position: 'relative'
    },
    container: {
      display: 'flex',
      maxWidth: '800px',
      gap: '30px'
    },
    posterImageContainer: {
      width: '150px',
      height: '200px',
      backgroundColor: '#a6a6a6',
      borderRadius: '8px',
      flexShrink: 0
    },
    posterImage: {
      width: '100%',
      height: '100%',
      objectFit: 'cover',
      borderRadius: '8px'
    },
    contentArea: {
      flex: 1
    },
    posterTitle: {
      position: 'absolute',
      top: '30px',
      left: '189px',
      fontSize: '20px',
      fontWeight: 600,
      color: '#FFFFFF',
      margin: 0
    },
    price: {
      position: 'absolute',
      top: '98px',
      left: '189px',
      fontSize: '16px',
      fontWeight: 500,
      color: '#FFFFFF'
    },
    sizeLabel: {
      position: 'absolute',
      top: '128px',
      left: '189px',
      fontSize: '14px',
      fontWeight: 500,
      color: '#FFFFFF'
    },
    sizeButtons: {
      position: 'absolute',
      top: '148px',
      left: '189px',
      display: 'flex',
      gap: '8px'
    },
    sizeBtn: {
      width: '40px',
      height: '32px',
      backgroundColor: '#a6a6a6',
      border: 'none',
      borderRadius: '6px',
      fontSize: '12px',
      fontWeight: 500,
      color: '#1c1c1b',
      cursor: 'pointer',
      transition: 'all 0.2s ease'
    },
    sizeBtnActive: {
      backgroundColor: '#FFFFFF',
      color: '#1c1c1b',
      fontWeight: 600
    },
    frameLabel: {
      position: 'absolute',
      top: '190px',
      left: '189px',
      fontSize: '14px',
      fontWeight: 500,
      color: '#FFFFFF'
    },
    frameButtons: {
      position: 'absolute',
      top: '210px',
      left: '189px',
      display: 'flex',
      gap: '4px'
    },
    frameBtn: {
      padding: '6px 8px',
      backgroundColor: '#a6a6a6',
      border: 'none',
      borderRadius: '6px',
      fontSize: '10px',
      fontWeight: 400,
      color: '#1c1c1b',
      cursor: 'pointer',
      transition: 'all 0.2s ease'
    },
    frameBtnActive: {
      backgroundColor: '#FFFFFF',
      color: '#1c1c1b',
      fontWeight: 600
    },
    addToCartBtn: {
      position: 'absolute',
      top: '248px',
      left: '189px',
      width: '185px',
      height: '36px',
      backgroundColor: '#a6a6a6',
      border: 'none',
      borderRadius: '8px',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      fontSize: '13px',
      fontWeight: 600,
      color: '#1c1c1b',
      cursor: 'pointer',
      transition: 'all 0.2s ease'
    },
    buyNowBtn: {
      position: 'absolute',
      top: '288px',
      left: '189px',
      width: '185px',
      height: '36px',
      backgroundColor: '#a6a6a6',
      border: 'none',
      borderRadius: '8px',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      fontSize: '13px',
      fontWeight: 600,
      color: '#1c1c1b',
      cursor: 'pointer',
      transition: 'all 0.2s ease'
    },
    detailsTitle: {
      position: 'absolute',
      top: '340px',
      left: '30px',
      fontSize: '18px',
      fontWeight: 600,
      color: '#FFFFFF'
    },
    detailsSection: {
      position: 'absolute',
      top: '370px',
      left: '30px',
      width: '400px'
    },
    table: {
      width: '100%',
      borderCollapse: 'collapse',
      backgroundColor: '#1c1c1b'
    },
    tableRow: {
      borderBottom: '1px solid #a6a6a6'
    },
    tableHeader: {
      fontSize: '14px',
      fontWeight: 600,
      color: '#FFFFFF',
      padding: '8px 12px',
      textAlign: 'left',
      backgroundColor: '#a6a6a6',
      color: '#1c1c1b'
    },
    tableCell: {
      fontSize: '12px',
      fontWeight: 400,
      color: '#a6a6a6',
      padding: '6px 12px',
      verticalAlign: 'top'
    },
    tableCellBold: {
      fontSize: '12px',
      fontWeight: 600,
      color: '#FFFFFF',
      padding: '6px 12px',
      verticalAlign: 'top'
    }
  };

  return (
    <div style={styles.page}>
      <div style={styles.posterImageContainer}>
        <img 
          src="https://res.cloudinary.com/dxv6byz2q/image/upload/v1755676740/Smoking_Chills_Red_text_s93bz4.jpg" 
          alt="Smoking Chills Red" 
          style={styles.posterImage}
        />
      </div>
      
      <div style={styles.posterTitle}>Smoking Chills Red</div>
      
      <div style={styles.price}>₹ {currentPrice}.00</div>
      
      <div style={styles.sizeLabel}>Size:</div>
      <div style={styles.sizeButtons}>
        <button 
          style={{
            ...styles.sizeBtn,
            ...(selectedSize === 'A4' ? styles.sizeBtnActive : {})
          }}
          onClick={() => handleSizeChange('A4')}
        >
          A4
        </button>
        <button 
          style={{
            ...styles.sizeBtn,
            ...(selectedSize === 'A3' ? styles.sizeBtnActive : {})
          }}
          onClick={() => handleSizeChange('A3')}
        >
          A3
        </button>
      </div>
      
      <div style={styles.frameLabel}>Frame:</div>
      <div style={styles.frameButtons}>
        <button 
          style={{
            ...styles.frameBtn,
            ...(selectedFrame === 'no' ? styles.frameBtnActive : {})
          }}
          onClick={() => handleFrameChange('no')}
        >
          No frame
        </button>
        <button 
          style={{
            ...styles.frameBtn,
            ...(selectedFrame === 'black' ? styles.frameBtnActive : {})
          }}
          onClick={() => handleFrameChange('black')}
        >
          Black frame
        </button>
        <button 
          style={{
            ...styles.frameBtn,
            ...(selectedFrame === 'white' ? styles.frameBtnActive : {})
          }}
          onClick={() => handleFrameChange('white')}
        >
          White frame
        </button>
      </div>
      
      <button style={styles.addToCartBtn}>Add to cart</button>
      <button style={styles.buyNowBtn}>Buy now</button>
      
      <div style={styles.detailsTitle}>Poster Details</div>
      
      <div style={styles.detailsSection}>
        <table style={styles.table}>
          <thead>
            <tr style={styles.tableRow}>
              <th style={styles.tableHeader}>Specification</th>
              <th style={styles.tableHeader}>Details</th>
            </tr>
          </thead>
          <tbody>
            <tr style={styles.tableRow}>
              <td style={styles.tableCellBold}>Sizes</td>
              <td style={styles.tableCell}>A4 → 8.3 x 11.7 in<br/>A3 → 11.7 x 16.5 in</td>
            </tr>
            <tr style={styles.tableRow}>
              <td style={styles.tableCellBold}>Paper</td>
              <td style={styles.tableCell}>300 GSM premium art board<br/>Thick, durable & long-lasting</td>
            </tr>
            <tr style={styles.tableRow}>
              <td style={styles.tableCellBold}>Frame Choices</td>
              <td style={styles.tableCell}>No Frame (poster only)<br/>Black/White Frame (fiberwood, matte, 0.75 in)</td>
            </tr>
            <tr style={styles.tableRow}>
              <td style={styles.tableCellBold}>Dimensions with Frame</td>
              <td style={styles.tableCell}>A4 → ~9.8 x 13.2 in<br/>A3 → ~13.2 x 18 in</td>
            </tr>
            <tr style={styles.tableRow}>
              <td style={styles.tableCellBold}>Finish</td>
              <td style={styles.tableCell}>Smooth matte look<br/>Sharp & vibrant colors</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default Poster1;