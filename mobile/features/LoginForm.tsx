import React from 'react';
import { TextInput, View } from 'react-native';
import { Button } from '../components/Button';
import { Input } from '../components/Input';
import { Stack } from '../components/Stack';
import { Text } from '../components/Text';

export function LoginForm () {
    return (
        <View>
            <Input label='Email' placeholder='Your Email' icon='user' />
            <Input label='Password' placeholder='Your Password' icon='lock' />

            <Stack gap={15}>
                <Text>Forgot password?</Text>
                <Button variant='fill'>Sign In</Button>
                <Button variant='outline'>Sign Up</Button>
            </Stack>
        </View>
    )
}