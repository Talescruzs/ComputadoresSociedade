import React from 'react';
import { SafeAreaView, ScrollView, View, Text, Image, StyleSheet } from 'react-native';

export default function App() {
  return (
    <SafeAreaView style={styles.container}>
      <ScrollView>
        <Text style={styles.title}>ComputadoresSociedade</Text>
        <Text style={styles.subtitle}>Repositório destinado a armazenar os códigos do aplicativo da cadeira de computadores e sociedade.</Text>
        <Text style={styles.section}>Diagrama da coleta (teórica) dos dados de pessoas dentro dos ônibus</Text>
        <Image source={require('./imgs/Diagrama_fluxo_coleta.jpg')} style={styles.image} />
        <Text style={styles.section}>Diagrama do banco de dados</Text>
        <Image source={require('./imgs/Diagrama_banco.jpg')} style={styles.image} />
      </ScrollView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#fff',
  },
  title: {
    fontSize: 28,
    fontWeight: 'bold',
    margin: 16,
    textAlign: 'center',
  },
  subtitle: {
    fontSize: 16,
    marginHorizontal: 16,
    marginBottom: 16,
    textAlign: 'center',
  },
  section: {
    fontSize: 18,
    fontWeight: 'bold',
    marginTop: 24,
    marginHorizontal: 16,
  },
  image: {
    width: '90%',
    height: 200,
    resizeMode: 'contain',
    alignSelf: 'center',
    marginVertical: 16,
  },
});