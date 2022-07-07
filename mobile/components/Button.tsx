import React from 'react';
import { StyleSheet, TouchableOpacity } from 'react-native';
import { Text } from './Text';

interface IButtonProps {
    variant?: 'fill' | 'outline';
}

export function Button (props: React.PropsWithChildren<IButtonProps>) {
    return (
        <TouchableOpacity style={{
            ...styles.buttonView,
            backgroundColor: (props.variant ?? 'fill') === 'fill' ? '#457b9d' : '#fff'
        }}>
            <Text style={{
                color: (props.variant ?? 'fill') === 'fill' ? '#fff' : '#457b9d'
            }}>{props.children}</Text>
        </TouchableOpacity>
    )
}

const styles = StyleSheet.create({
    buttonView: {
        borderRadius: 7,
        borderColor: "#457b9d",
        borderWidth: 1,
        alignItems: "center",
        justifyContent: "center",
        padding: 10
    },
})