/*******************************************************************************
 * Copyright (c) 2015 Matthijs Kooijman
 * All rights reserved. This program and the accompanying materials
 * are made available under the terms of the Eclipse Public License v1.0
 * which accompanies this distribution, and is available at
 * http://www.eclipse.org/legal/epl-v10.html
 *
 * This the HAL to run LMIC on top of the Arduino environment.
 *******************************************************************************/
#ifndef _localhal_hal_h_
#define _localhal_hal_h_

static const int NUM_DIO = 3;

#define UNUSED_PIN 255

struct lmic_pinmap {
    u1_t nss;
    u1_t rxtx;
    u1_t rst;
    u1_t dio[NUM_DIO];
};

// Declared here, to be defined an initialized by the application
extern lmic_pinmap pins;

#endif // _localhal_hal_h_

