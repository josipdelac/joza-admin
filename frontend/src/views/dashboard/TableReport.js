import React from 'react';
import {
  Document,
  Page,
  Text,
  View,
  StyleSheet,
  PDFViewer,
} from '@react-pdf/renderer';

const styles = StyleSheet.create({
  page: {
    flexDirection: 'row',
    backgroundColor: '#E4E4E4',
  },
  section: {
    margin: 10,
    padding: 10,
    flexGrow: 1,
  },
  table: {
    display: 'table',
    width: 'auto',
    borderStyle: 'solid',
    borderColor: '#bfbfbf',
    borderWidth: 1,
    borderRightWidth: 0,
    borderBottomWidth: 0,
  },
  tableRow: {
    flexDirection: 'row',
  },
  tableCol: {
    width: '20%',
    borderStyle: 'solid',
    borderColor: '#bfbfbf',
    borderWidth: 1,
    borderLeftWidth: 0,
    borderTopWidth: 0,
    padding: 5,
  },
  cell: {
    fontSize: 10,
  },
});

const TableReport = ({ robotEntries }) => {
  const currentDate = new Date().toLocaleDateString();

  return (
    <Document>
    
      <Page size="A4" style={styles.page}>
        <View style={styles.section}>
        <Text style={{ fontSize: 16, marginBottom: 10, textAlign: 'center' }}>
           Robot statistics for {currentDate}
          </Text>
          <View style={styles.table}>
            <View style={styles.tableRow}>
              
              <View style={styles.tableCol}>
                <Text style={styles.cell}>Robot Name</Text>
              </View>
              <View style={styles.tableCol}>
                <Text style={styles.cell}>Status</Text>
              </View>
              <View style={styles.tableCol}>
                <Text style={styles.cell}>Progress</Text>
              </View>
              <View style={styles.tableCol}>
                <Text style={styles.cell}>Server</Text>
              </View>
              <View style={styles.tableCol}>
                <Text style={styles.cell}>Last Updated</Text>
              </View>
            </View>
            {robotEntries.map((item, index) => (
              <View style={styles.tableRow} key={index}>
                
                <View style={styles.tableCol}>
                  <Text style={styles.cell}>{item.name}</Text>
                </View>
                <View style={styles.tableCol}>
                  <Text style={styles.cell}>{item.status}</Text>
                </View>
                <View style={styles.tableCol}>
                  <Text style={styles.cell}>{item.current_item}/{item.total_items}</Text>
                </View>
                <View style={styles.tableCol}>
                  <Text style={styles.cell}>{item.server_id}</Text>
                </View>
                <View style={styles.tableCol}>
                  <Text style={styles.cell}>{item.datum}</Text>
                </View>
              </View>
            ))}
          </View>
        </View>
      </Page>
    </Document>
  );
};

export default TableReport;
