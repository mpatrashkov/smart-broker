import React from 'react';
import { StyleSheet, TextInput, View } from 'react-native';
import { Text } from './Text';
import FontAwesome5 from 'react-native-vector-icons/FontAwesome5';
import { utils } from '../styles/utils';

interface IInputProps {
    label: string;
    placeholder: string;
    icon: string;
}

export function Input (props: IInputProps) {
    return (
        <View style={styles.container}>
            <Text>{props.label}</Text>
            <View style={{ ...utils.row, ...styles.inputView }}>
                <FontAwesome5 name={props.icon} solid />
                <TextInput style={{
                    paddingLeft: 10
                }} placeholder={props.placeholder} />
            </View>
        </View>
    )
}

const styles = StyleSheet.create({
    container: {
        paddingVertical: 10
    },
    inputView: {
        borderBottomColor: '#ccc',
        borderBottomWidth: 1,
    }
})